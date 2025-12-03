import tkinter as tk
import numpy as np
import matplotlib.image as mpimg
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import ast
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from matplotlib import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BuscaP import busca

class App():
    #--------------------------------------------------------------------------
    # Criar a janela principal
    #--------------------------------------------------------------------------
    def __init__(self, janela):
        self.janela = janela
        self.canvas = None
        self.busca = busca()

        # Estilo da janela
        self.janela.grid_columnconfigure(2, weight=1)
        self.janela.grid_rowconfigure(8, weight=1)
        self.janela.configure(background='#dfe3ee')
        self.janela.minsize(700, 600)

        # Produtos
        self.produtos = {
            0: "Minério de ferro - (7, 7)",
            1: "Carvão mineral - (2, 6)",
            2: "Tubos - (7, 3)",
            3: "Ligas metálicas - (3, 6)",
            4: "Óleos lubrificantes - (5, 2)",
            5: "Placas de aço - (2, 4)",
            6: "Chapas laminadas a frio - (5, 6)",
            7: "EPIs (luvas, óculos, máscaras para solda) - (2, 2)",
            8: "Parafusos, porcas e arruelas - (3, 2)",
            9: "Areia de moldagem - (5, 3)",
            10: "Resina - (7, 2)",
        }

        self.frame = tk.Frame(self.janela, bg="white")
        self.frame.grid(row=0, column=0, rowspan=9, columnspan=2, sticky="nsew")

        # Estilo frame
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(9, weight=1)

        style = ttk.Style()
        style.map("Custom.TCombobox",
            fieldbackground=[("readonly", "#ffffff"), ("disabled", "#B2B4BA")],
            foreground=[("readonly", "black"), ("disabled", "gray")]
        )

        # Label
        self.label = ttk.Label(self.frame, text="Selecione os campos abaixo:", bootstyle="warning")
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Listbox
        self.lista_produtos = tk.Listbox(
            self.frame, 
            selectmode="multiple", 
            width=50, 
            height=10,
            font=("Arial", 11)
        )
        self.lista_produtos.grid(row=1, column=0, sticky="nsew", padx=10)

        # Inserir os produtos
        for cod, nome in self.produtos.items():
            self.lista_produtos.insert(tk.END, f"{cod} - {nome}")

        # Botão
        self.botao = ttk.Button(self.frame, text="Obter Valor", command=self.obter_valor_selecionado, bootstyle=(WARNING, OUTLINE))
        self.botao.grid(row=7, column=0, padx=20, pady=20, sticky="ew")

    def obter_valor_selecionado(self):
        #origem - (porta do armazém)
        origem = (3,0)

        # Produtos selecionados
        selecionados = self.lista_produtos.curselection()
        if not selecionados:
            print("Nenhum produto selecionado")
            return

        # Arquivo e mapa
        arquivo = "mapa.txt"
        mapa, nx, ny = self.busca.Gera_Problema_Grid_Fixo(arquivo)

        # Converte para posição no grid
        posicoes = {}
        arq = open("posicoes.txt")
        for aux in arq:
            linha = aux.strip().split()
            if len(linha) == 3:
                chave = linha[0]
                x = int(linha[1])
                y = int(linha[2])
                posicoes[chave] = (x, y)
                
        # Possíveis posições no mapa
        posicoes_inv = {v: k for k,v in posicoes.items()}   

        #1) pega apenas as posições dos produtos
        locais_produtos = []
        for id in selecionados:
            for indice, pos in posicoes.items():
                if(int(indice) == id):
                    locais_produtos.append(pos)

        #2) Ordenar pontos pela proximidade da origem (OK, mantemos a ordem)
        locais_produtos.sort(key=lambda p: abs(p[0]-origem[0]) + abs(p[1]-origem[1]))

        #3) Executar A* entre origem → P1 → P2 → ...
        mapa_temp_inicial = [linha[:] for linha in mapa]  # mapa original

        #4) Pega o nome dos produtos selecionados
        produtos_selecionado = []
        for id in selecionados:
            for indice in self.produtos:
                if(int(indice) == id):
                    produtos_selecionado.append(self.produtos[indice])

        caminho_total = []
        caminho_str = []

        for destino in locais_produtos:
            # copia o mapa original
            mapa_temp = [linha[:] for linha in mapa_temp_inicial]

            # libera APENAS o destino atual
            x, y = destino
            mapa_temp[x][y] = 0    # destino precisa ser alcançável

            # A* entre origem → destino
            caminho = self.busca.a_estrela(origem, destino, mapa_temp, nx, ny)

            if caminho:
                for ps in produtos_selecionado:
                    c = ast.literal_eval(ps.split(" - ")[1])
                    c_inv = (c[1], c[0])
                    
                    if(str(caminho[len(caminho)-1]) == str(c_inv)):
                        caminho_str.append(ps.split(" - ")[0])
                        
            else:
                caminho_str.append("Caminho não encontrado")

            if not caminho:
                print(f"Sem caminho possível entre {origem} → {destino}! Tentando próximo produto.")
                # apenas pula para o próximo
                origem = destino
                continue

            # adiciona ao caminho total 
            if not caminho_total:
                caminho_total.extend(caminho)
            else:
                caminho_total.extend(caminho[1:])

            # agora este produto deixa de ser obstáculo!
            mapa_temp_inicial[x][y] = 0

            origem = destino

        fig = Figure(figsize=(1, 1), dpi=100, facecolor="#dfe3ee")
        plot_fig = fig.add_subplot(111)

        # Ajustar mapa para matriz homogênea
        largura_max = max(len(linha) for linha in mapa)
        mapa = np.array([linha + [9] * (largura_max - len(linha)) for linha in mapa])

        # Cores personalizadas
        cores = ["#ffffff", "#dcdcdc"]  
        cmap_custom = ListedColormap(cores)

        # Converter 0 e 9 para índices do colormap
        mapa_convertido = mapa.copy()
        mapa_convertido[mapa_convertido == 0] = 0
        mapa_convertido[mapa_convertido == 9] = 1

        plot_fig.imshow(
            mapa_convertido,
            cmap=cmap_custom,
            origin="lower",
            extent=[0, ny, 0, nx]
        )

        # Grid correto
        plot_fig.set_xlim(0, ny)
        plot_fig.set_ylim(0, nx)

        # linhas do grid
        for y in range(nx + 1):
            plot_fig.axvline(y, color="black", linewidth=0.5)
        for x in range(ny + 1):
            plot_fig.axhline(x, color="black", linewidth=0.5)

        if caminho_total:
            origem_fixa = (3, 0)

            xs, ys = zip(*caminho_total)

            xs_plot = [x + 0.5 for x in xs]
            ys_plot = [y + 0.5 for y in ys]

            plot_fig.plot(ys_plot, xs_plot, color="red", linewidth=2, markersize=4)

            # Plota Origem
            plot_fig.annotate(
                "Origem",
                xy=(origem_fixa[1] + 0.5, origem_fixa[0] + 0.5),
                xytext=(origem_fixa[1] + 0.8, origem_fixa[0] + 0.2),
                arrowprops=dict(facecolor="green", shrink=0.05, width=2, headwidth=8),
                fontsize=10,
                color="green"
            )

        # --- Plotar produtos com a cor certa ---
        for cod, pos in zip(selecionados, locais_produtos):
            x, y = pos
            cor_produto = (0, 0, 0)  # cor fixa

            plot_fig.scatter(
                y + 0.5, x + 0.5,
                s=120,
                facecolor=cor_produto,   # ← usa a cor fixa
                edgecolor="black",
                linewidth=1.2
            )


        # Se houver caminho, desenha em vermelho
        if caminho and len(caminho) > 0:
            xs, ys = zip(*caminho)

        # Inserir no Tkinter (grid) — substitui se já existir
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.janela) # Use self.janela
        self.canvas.get_tk_widget().grid(row=2, column=2, rowspan=7, padx=10, pady=0, sticky="nsew")

        # Exibe no Tkinter
        if hasattr(self, "caminho_label") and self.caminho_label is not None:
            self.caminho_label.destroy()

        if caminho is None:
            texto = caminho_str
            cor = "red"
        else:
            lista_produtos = "\n".join([f"{i+1}º {item}" for i, item in enumerate(caminho_str)])
            texto = f"Ordem de entrega dos produtos: \n {lista_produtos}"
            cor = "black"

        # Cria/atualiza a label
        self.caminho_label = tk.Label(self.frame, text=texto, font=("Arial", 12), fg=cor, background="#ffffff",wraplength=650, justify="left")
        self.caminho_label.grid(row=8, column=0, columnspan=1, padx=2 , sticky="ew")

# -------------------------
# CRIAR A JANELA E INICIAR
# -------------------------
if __name__ == "__main__":
    janela = ttk.Window(themename="superhero")
    janela.title("Métodos de Busca")
    app = App(janela)
    janela.mainloop()
