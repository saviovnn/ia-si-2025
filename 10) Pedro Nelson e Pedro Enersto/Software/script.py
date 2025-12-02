import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from BuscaNP import buscaNP
from BuscaP import busca

df = pd.read_csv("grafo.csv", index_col=0, encoding="latin1")
nos = list(df.index)

grafo_nao_ponderado = []
for i, origem in enumerate(nos):
    adj = []
    for j, destino in enumerate(nos):
        if df.iloc[i, j] != 0:
            adj.append(destino)
    grafo_nao_ponderado.append(adj)

grafo_ponderado_lista = []
for i, origem in enumerate(nos):
    sucessores_com_peso = []
    for j, destino in enumerate(nos):
        peso = df.iloc[i, j]
        if peso != 0:
            sucessores_com_peso.append((destino, float(peso)))
    grafo_ponderado_lista.append([0, sucessores_com_peso])

G = nx.Graph()
for origem in df.index:
    for destino in df.columns:
        if df.loc[origem, destino] != 0:
            G.add_edge(origem, destino, weight=float(df.loc[origem, destino]))

pos_geografico = { 
"Angra dos Reis": (-44.31, -23.00), "Bananal": (-44.32, -22.68),
"Porto Real": (-44.29, -22.41), "Itatiaia": (-44.56, -22.49),
"Cruzeiro": (-44.96, -22.57), "Cachoeira Paulista": (-45.00, -22.66),
"Lorena": (-45.12, -22.73), "Guaratingueta": (-45.19, -22.81),
"Aparecida": (-45.22, -22.84), "Tremembe": (-45.54, -22.95),
"Taubate": (-45.55, -23.02), "Cacapava": (-45.70, -23.09),
"Sao Jose dos Campos": (-45.88, -23.17), "Jacarei": (-45.96, -23.30),
"Guarulhos": (-46.53, -23.45), "Suzano": (-46.31, -23.54),
"Mogi das Cruzes": (-46.18, -23.52), "Santa Branca": (-45.88, -23.39),
"Paraibuna": (-45.66, -23.38), "Sao Luiz do Paraitinga": (-45.31, -23.22),
"Natividade da Serra": (-45.44, -23.37), "Ubatuba": (-45.07, -23.43),
"Paraty": (-44.71, -23.21), "Lagoinha": (-45.18, -23.08),
"Campos do Jordao": (-45.59, -22.73), "Itajuba": (-45.45, -22.42),
"Paraisopolis": (-45.78, -22.67), "Extrema": (-46.31, -22.85),
"Braganca Paulista": (-46.54, -22.95), "Atibaia": (-46.55, -23.11),
"Arapei": (-44.44, -22.67), "Areias": (-44.70, -22.57),
"Canas": (-45.05, -22.70), "Caraguatatuba": (-45.41, -23.62),
"Cunha": (-44.95, -23.07), "Igarata": (-46.15, -23.20),
"Ilhabela": (-45.35, -23.77), "Jambeiro": (-45.69, -23.25),
"Monteiro Lobato": (-45.84, -22.95), "Pindamonhangaba": (-45.46, -22.92),
"Piquete": (-45.17, -22.61), "Potim": (-45.24, -22.84),
"Queluz": (-44.77, -22.52), "Redencao da Serra": (-45.57, -23.27),
"Roseira": (-45.30, -22.89), "Santo Antonio do Pinhal": (-45.66, -22.82),
"Sao Bento do Sapucai": (-45.73, -22.68), "Sao Jose do Barreiro": (-44.60, -22.64),
"Sao Sebastiao": (-45.41, -23.80), "Silveiras": (-44.85, -22.66)


 }
pos = {city: (lon, -lat) for city, (lon, lat) in pos_geografico.items()}

class GraphApp:
    def __init__(self, root, G, nos, grafo_nao_ponderado, grafo_ponderado_lista):
        self.root = root
        self.G = G
        self.nos = nos
        self.grafo_nao_ponderado = grafo_nao_ponderado
        self.grafo_ponderado_lista = grafo_ponderado_lista

        self.buscadorNP = buscaNP()
        self.buscadorP = busca()

        self.root.title("Busca em Grafos - IA")
        self.root.state('zoomed')

        root.columnconfigure(2, weight=1)
        root.rowconfigure(0, weight=1)

        control_frame = ttk.Frame(root, padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky="nw")

        ttk.Label(control_frame, text="Início:").grid(row=0, column=0, sticky="w", pady=5)
        self.start_cb = ttk.Combobox(control_frame, values=self.nos, width=25)
        self.start_cb.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(control_frame, text="Fim:").grid(row=1, column=0, sticky="w", pady=5)
        self.end_cb = ttk.Combobox(control_frame, values=self.nos, width=25)
        self.end_cb.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(control_frame, text="Método:").grid(row=2, column=0, sticky="w", pady=5)
        self.method_cb = ttk.Combobox(
            control_frame,
            values=[
                "Busca em Largura", "Busca em Profundidade", "Profundidade Limitada",
                "Aprofundamento iterativo", "Busca Bidirecional", "Custo Uniforme",
                "Greedy", "A*", "AIA*"
            ],
            width=25
        )
        self.method_cb.grid(row=2, column=1, pady=5, padx=5)
        self.method_cb.bind("<<ComboboxSelected>>", self.on_method_change)

        # Caixa para definir o Limite (inicialmente invisível)
        self.limit_label = ttk.Label(control_frame, text="Limite:")
        self.limit_cb = ttk.Combobox(control_frame, values=[str(i) for i in range(1, 43)], width=25)

        self.btn = ttk.Button(control_frame, text="Executar Busca", command=self.run_search)
        self.btn.grid(row=4, column=0, columnspan=2, pady=15)

        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=10, sticky="nsew", padx=10, pady=10)

        self.info_frame = ttk.Frame(root, padding="8")
        self.info_frame.grid(row=1, column=2, sticky="se", padx=10, pady=(0, 10))
        self.info_title = ttk.Label(self.info_frame, text="Resultado", font=("Segoe UI", 10, "bold"))
        self.info_title.grid(row=0, column=0, sticky="w")
        self.info_text = tk.Text(self.info_frame, width=45, height=5, wrap="word", state="disabled")
        self.info_text.grid(row=1, column=0, sticky="nsew", pady=(5, 0))

        self.draw_graph()

    def on_method_change(self, event=None):
        metodo = self.method_cb.get()
        if metodo == "Profundidade Limitada":
            self.limit_label.grid(row=3, column=0, sticky="w", pady=5)
            self.limit_cb.grid(row=3, column=1, pady=5, padx=5)
        else:
            self.limit_label.grid_remove()
            self.limit_cb.grid_remove()

    def update_info_box(self, path, cost, limit=None):
        if not path:
            txt = "Nenhum caminho encontrado."
        else:
            caminho_str = " -> ".join(path)
            if cost is None:
                total = 0.0
                for u, v in zip(path, path[1:]): 
                    w = self.G[u][v].get('weight', 0)
                    total += float(w)
                cost = total
            if limit is not None:
                txt = f"Caminho: {caminho_str}\nDistância total: {cost:.2f} km"
            else:
                txt = f"Caminho: {caminho_str}\nDistância total: {cost:.2f} km"
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, txt)
        self.info_text.config(state="disabled")

    def run_search(self):
        inicio = self.start_cb.get()
        fim = self.end_cb.get()
        metodo = self.method_cb.get()
        limite = self.limit_cb.get() if metodo == "Profundidade Limitada" else None

        if not inicio or not fim or not metodo or (metodo == "Profundidade Limitada" and not limite):
            messagebox.showwarning("Aviso", "Por favor, selecione início, fim, método de busca e limite (quando necessário).")
            return

        path = []
        cost = None
        limit = None

        try:
            if metodo in ["Busca em Largura", "Busca em Profundidade", "Profundidade Limitada", "Aprofundamento iterativo", "Busca Bidirecional"]:
                if metodo == "Busca em Largura":
                    path = self.buscadorNP.amplitude(inicio, fim, self.nos, self.grafo_nao_ponderado)
                elif metodo == "Busca em Profundidade":
                    path = self.buscadorNP.profundidade(inicio, fim, self.nos, self.grafo_nao_ponderado)
                elif metodo == "Profundidade Limitada":
                    lim = int(limite)
                    path = self.buscadorNP.prof_limitada(inicio, fim, self.nos, self.grafo_nao_ponderado, lim=lim)
                    limit = lim
                elif metodo == "Aprofundamento iterativo":
                    path = self.buscadorNP.aprof_iterativo(inicio, fim, self.nos, self.grafo_nao_ponderado, lim_max=43)
                elif metodo == "Busca Bidirecional":
                    path = self.buscadorNP.bidirecional(inicio, fim, self.nos, self.grafo_nao_ponderado)
            else:
                if metodo == "Custo Uniforme":
                    path, cost = self.buscadorP.custo_uniforme(inicio, fim, self.nos, self.grafo_ponderado_lista)
                elif metodo == "Greedy":
                    path, cost = self.buscadorP.greedy(inicio, fim, self.nos, self.grafo_ponderado_lista)
                elif metodo == "A*":
                    path, cost = self.buscadorP.a_estrela(inicio, fim, self.nos, self.grafo_ponderado_lista)
                elif metodo == "AIA*":
                    path, cost, limit = self.buscadorP.aia_estrela(inicio, fim, self.nos, self.grafo_ponderado_lista)

            self.update_info_box(path, cost, limit)
        except Exception as e:
            messagebox.showerror("Erro na Busca", f"Ocorreu um erro durante a execução da busca: {e}")
            self.draw_graph()
            return

        if path:
            self.draw_graph(path)
        else:
            messagebox.showinfo("Resultado", f"Não foi encontrado um caminho de '{inicio}' para '{fim}'.")
            self.draw_graph()

    def draw_graph(self, path=None):
        self.ax.clear()
        nx.draw(
            self.G, pos, with_labels=True, ax=self.ax,
            node_size=400, node_color='#a0e0f0',
            font_size=8, edge_color='gray'
        )
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax, font_size=7)
        if path and len(path) > 1:
            edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(self.G, pos, nodelist=path, node_color='red', ax=self.ax, node_size=500)
            nx.draw_networkx_edges(self.G, pos, edgelist=edges, edge_color='red', width=2.5, ax=self.ax)
        self.ax.set_title("Mapa de Cidades e Rotas")
        self.ax.invert_yaxis()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root, G, nos, grafo_nao_ponderado, grafo_ponderado_lista)
    root.mainloop()
