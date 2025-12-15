import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import heapq
import json
from BuscaNP import buscaNP  
import matplotlib.patches as mpatches

# ---------------------------------------------------------
# FUNÇÃO PARA LER O GRAFO CORRIGIDA
# ---------------------------------------------------------
def ler_grafo(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    grafo = {}
    nos = []

    if "," in linhas[0]:  
        for linha in linhas:
            dados = [d.strip() for d in linha.split(",") if d.strip()]
            no = dados[0]
            nos.append(no)
            vizinhos = []
            i = 1
            
            # Verificar quantos valores temos por vizinho
            while i < len(dados):
                if i + 2 < len(dados):  # Temos 3 valores: vizinho, distância, tempo
                    viz = str(dados[i])
                    dist = int(dados[i + 1])
                    tempo = int(dados[i + 2])
                    vizinhos.append((viz, dist, tempo))
                    i += 3
                elif i + 1 < len(dados):  # Temos apenas 2 valores: vizinho, peso
                    viz = str(dados[i])
                    peso = int(dados[i + 1])
                    # Usar o mesmo valor para distância e tempo
                    vizinhos.append((viz, peso, peso))
                    i += 2
                else:
                    # Apenas um valor (apenas vizinho)
                    viz = str(dados[i])
                    vizinhos.append((viz, 1, 1))  # Valores padrão
                    i += 1
                    
            grafo[no] = vizinhos
    else:  
        # Para grafos básicos sem vírgulas
        nos = linhas[0].split()
        for i, linha in enumerate(linhas[1:]):
            no = nos[i]
            grafo[no] = []
            valores = linha.split()
            j = 0
            while j < len(valores):
                if j + 2 < len(valores):  # 3 valores
                    viz = str(valores[j])
                    dist = int(valores[j + 1])
                    tempo = int(valores[j + 2])
                    grafo[no].append((viz, dist, tempo))
                    j += 3
                elif j + 1 < len(valores):  # 2 valores
                    viz = str(valores[j])
                    peso = int(valores[j + 1])
                    grafo[no].append((viz, peso, peso))
                    j += 2
                else:  # 1 valor
                    viz = str(valores[j])
                    grafo[no].append((viz, 1, 1))
                    j += 1

    return grafo, nos

# ---------------------------------------------------------
# FUNÇÕES PARA SALVAR E CARREGAR POSIÇÕES
# ---------------------------------------------------------
def salvar_posicoes(posicoes, arquivo_posicoes):
    posicoes_serializaveis = {}
    for node, pos in posicoes.items():
        if hasattr(pos, 'tolist'):
            posicoes_serializaveis[node] = pos.tolist()
        else:
            posicoes_serializaveis[node] = [float(pos[0]), float(pos[1])]
    
    with open(arquivo_posicoes, 'w', encoding='utf-8') as f:
        json.dump(posicoes_serializaveis, f, indent=2)

def carregar_posicoes(arquivo_posicoes):
    if os.path.exists(arquivo_posicoes):
        with open(arquivo_posicoes, 'r', encoding='utf-8') as f:
            posicoes_carregadas = json.load(f)
            return {node: tuple(pos) for node, pos in posicoes_carregadas.items()}
    return None

# ---------------------------------------------------------
# CLASSE BUSCA NP CORRIGIDA
# ---------------------------------------------------------
class BuscaNPCorrigida(buscaNP):
    def __init__(self):
        super().__init__()
        self.heuristicaS = {}  # Cache para heurísticas calculadas
    
    def sucessores_grafo2_corrigido(self, ind, grafo, ordem):
        """
        Versão corrigida do sucessores_grafo2 para trabalhar com índices
        """
        f = []
        for suc in grafo[ind][::ordem]:
            if isinstance(suc, list) and len(suc) >= 3:
                vizinho_idx = suc[0]
                dist = suc[1]
                tempo = suc[2]
                f.append((vizinho_idx, dist, tempo))
            elif isinstance(suc, tuple) and len(suc) >= 3:
                vizinho_idx = suc[0]
                dist = suc[1]
                tempo = suc[2]
                f.append((vizinho_idx, dist, tempo))
        return f

    def heuristica(self, nos, grafo, destino_idx):
        """
        Calcula heurística usando Dijkstra para estimar distâncias até o destino
        Adaptada para trabalhar com índices numéricos
        """
        if destino_idx in self.heuristicaS:
            return self.heuristicaS[destino_idx]
        
        # Inicializar distâncias para todos os nós
        dist = {idx: float("inf") for idx in range(len(nos))}
        dist[destino_idx] = 0
        fila = [(0, destino_idx)]
        heapq.heapify(fila)
        
        while fila:
            custo_atual, atual_idx = heapq.heappop(fila)
            if custo_atual > dist[atual_idx]:
                continue
            
            # Recupera vizinhos do nó atual
            vizinhos = grafo[atual_idx]
            
            for vizinho_data in vizinhos:
                if len(vizinho_data) >= 2:
                    vizinho_idx = int(vizinho_data[0])
                    peso = int(vizinho_data[1])  # Usa distância como peso para heurística
                    novo_custo = custo_atual + peso
                    if novo_custo < dist[vizinho_idx]:
                        dist[vizinho_idx] = novo_custo
                        heapq.heappush(fila, (novo_custo, vizinho_idx))
        
        self.heuristicaS[destino_idx] = dist
        return dist
    
    def heuristica_grafo(self, nos, n_idx, destino_idx, grafo):
        """
        Retorna valor heurístico para um nó específico (usando índices)
        """
        heuristicas = self.heuristica(nos, grafo, destino_idx)
        return heuristicas.get(n_idx, float("inf"))

    def a_estrela_corrigido(self, inicio, fim, nos, grafo, MostrarRotas=True):
        """
        Versão do A* com heurística adaptada para índices numéricos
        """
        if inicio == fim:
            return [inicio], 0, 0

        # Usar uma fila de prioridade
        lista = []
        
        # Calcular heurística inicial
        h_inicio = self.heuristica_grafo(nos, inicio, fim, grafo)
        
        raiz = (h_inicio, inicio, 0, h_inicio, [inicio])  # (f, nó, g, h, caminho)
        heapq.heappush(lista, raiz)
        
        visitado = set()

        while lista:
            f, atual, g, h, caminho = heapq.heappop(lista)
            
            if atual in visitado:
                continue
                
            visitado.add(atual)

            if atual == fim:
                return caminho, g, g  # Retorna caminho, distância, tempo

            # Obter sucessores
            filhos = self.sucessores_grafo2_corrigido(atual, grafo, 1)
            
            for vizinho, dist, tempo in filhos:
                if vizinho in visitado:
                    continue
                    
                novo_g = g + dist
                novo_caminho = caminho + [vizinho]
                
                # Calcular heurística para o vizinho
                novo_h = self.heuristica_grafo(nos, vizinho, fim, grafo)
                novo_f = novo_g + novo_h
                
                heapq.heappush(lista, (novo_f, vizinho, novo_g, novo_h, novo_caminho))

        return None, float("inf"), float("inf")

    def rota_alternativa_corrigida(self, caminho_principal, inicio, fim, nos, grafo):
        """
        Remove temporariamente a aresta mais congestionada do caminho principal
        e calcula outra rota.
        """
        if len(caminho_principal) < 2:
            return None, float("inf"), float("inf")

        # Encontrar a aresta mais congestionada
        max_congestionamento = 0
        aresta_remover = None
        
        for i in range(len(caminho_principal) - 1):
            origem = caminho_principal[i]
            destino = caminho_principal[i + 1]
            
            # Encontrar dados da aresta
            for viz, dist, tempo in grafo[origem]:
                if viz == destino:
                    if dist > 0:
                        congestionamento = tempo / dist
                        if congestionamento > max_congestionamento:
                            max_congestionamento = congestionamento
                            aresta_remover = (origem, destino)
                    break

        if not aresta_remover:
            return None, float("inf"), float("inf")

        # Criar cópia do grafo
        grafo_temp = [list(linha) for linha in grafo]

        # Remover a aresta mais congestionada
        origem_idx, destino_idx = aresta_remover
        idx_origem = nos.index(origem_idx)
        
        # Remover a aresta na direção origem->destino
        grafo_temp[idx_origem] = [(v, d, t) for (v, d, t) in grafo_temp[idx_origem] if v != destino_idx]
        
        # Remover a aresta na direção destino->origem (para grafos não direcionados)
        idx_destino = nos.index(destino_idx)
        grafo_temp[idx_destino] = [(v, d, t) for (v, d, t) in grafo_temp[idx_destino] if v != origem_idx]

        # Executar nova busca
        return self.a_estrela_corrigido(inicio, fim, nos, grafo_temp)

# ---------------------------------------------------------
# CLASSE PRINCIPAL DA INTERFACE COM LEGENDAS COMPLETAS
# ---------------------------------------------------------
class InterfaceLogisticaCongestionamento:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Logística - Roteirização com Congestionamento")
        self.root.geometry("1400x900")

        # Configuração de estilo
        self.root.configure(bg="#1e3d59")
        style = ttk.Style()
        style.theme_use("clam")

        # Cores
        azul_escuro = "#1e3d59"
        azul_medio = "#2a4b6e"
        laranja_logistica = "#ff6b35"
        verde_sucesso = "#4caf50"
        texto_branco = "#ffffff"

        # Configurar estilos
        style.configure("TFrame", background=azul_escuro)
        style.configure("TLabel", background=azul_escuro, foreground=texto_branco, font=("Arial", 10))
        style.configure("Title.TLabel", background=azul_escuro, foreground=texto_branco, font=("Arial", 12, "bold"))
        style.configure("TLabelframe", background=azul_medio, foreground=texto_branco)
        style.configure("TButton", background=laranja_logistica, foreground=texto_branco, font=("Arial", 10))
        style.map("TButton", background=[("active", "#ff8c5a")])
        style.configure("Success.TButton", background=verde_sucesso)
        style.map("Success.TButton", background=[("active", "#6bc76b")])

        self.grafo = None
        self.nos = []
        self.busca_obj = BuscaNPCorrigida()
        self.caminho_ida = []
        self.caminho_alternativo = []
        self.posicoes = {}
        self.node_arrastando = None
        self.modo_edicao = False
        self.zoom_level = 1.0
        self.pan_start = None

        # Variáveis de controle
        self.file_var = tk.StringVar()
        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()
        self.method_var = tk.StringVar(value="A* (Tempo)")

        self.criar_interface()
        self.atualizar_lista_arquivos()

    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Logística - Roteirização com Congestionamento", 
                               style="Title.TLabel")
        title_label.pack(pady=(0, 10))

        # Container principal
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Painel de controle (esquerda)
        control_frame = ttk.LabelFrame(content_frame, text="Controle de Rotas", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Visualização do mapa (direita)
        graph_frame = ttk.LabelFrame(content_frame, text="Mapa de Rotas", padding=10)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configuração da Rota
        route_config_frame = ttk.LabelFrame(control_frame, text="Configuração da Rota", padding=10)
        route_config_frame.pack(fill=tk.X, pady=(0, 10))

        # Arquivo
        ttk.Label(route_config_frame, text="Rede de Cidades:").pack(anchor=tk.W)
        self.file_combo = ttk.Combobox(route_config_frame, textvariable=self.file_var, state="readonly")
        self.file_combo.pack(fill=tk.X, pady=(5, 10))
        self.file_combo.bind('<<ComboboxSelected>>', self.carregar_arquivo)

        # Origem e Destino
        ttk.Label(route_config_frame, text="Origem:").pack(anchor=tk.W)
        self.start_combo = ttk.Combobox(route_config_frame, textvariable=self.start_var)
        self.start_combo.pack(fill=tk.X, pady=(5, 10))

        ttk.Label(route_config_frame, text="Destino:").pack(anchor=tk.W)
        self.end_combo = ttk.Combobox(route_config_frame, textvariable=self.end_var)
        self.end_combo.pack(fill=tk.X, pady=(5, 10))

        # Botões de busca
        ttk.Button(route_config_frame, text="Calcular Rota Principal", 
                  command=self.executar_busca_principal, style="Success.TButton").pack(fill=tk.X, pady=5)

        ttk.Button(route_config_frame, text="Buscar Rota Alternativa", 
                  command=self.executar_busca_alternativa).pack(fill=tk.X, pady=5)

        # Controles de edição
        edit_frame = ttk.LabelFrame(control_frame, text="Edição do Mapa", padding=10)
        edit_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(edit_frame, text="Ativar Edição", 
                  command=self.ativar_edicao).pack(fill=tk.X, pady=2)
        ttk.Button(edit_frame, text="Desativar Edição", 
                  command=self.desativar_edicao).pack(fill=tk.X, pady=2)
        ttk.Button(edit_frame, text="Salvar Posições", 
                  command=self.salvar_posicoes_nodes).pack(fill=tk.X, pady=2)
        ttk.Button(edit_frame, text="Limpar Rotas", 
                  command=self.limpar_caminhos).pack(fill=tk.X, pady=2)
        ttk.Button(edit_frame, text="Resetar Zoom", 
                  command=self.resetar_zoom).pack(fill=tk.X, pady=2)

        # Console de saída
        console_frame = ttk.LabelFrame(control_frame, text="Log do Sistema", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.console_text = scrolledtext.ScrolledText(console_frame, height=15, 
                                                     bg="#0d2b47", fg="white", 
                                                     font=("Consolas", 9))
        self.console_text.pack(fill=tk.BOTH, expand=True)

        # Área do gráfico
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor="#1e3d59")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1e3d59")
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Conectar eventos do mouse
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("button_press_event", self.on_pan_start)
        self.canvas.mpl_connect("motion_notify_event", self.on_pan)
        self.canvas.mpl_connect("button_release_event", self.on_pan_end)

        self.log("Sistema iniciado. Selecione um arquivo de rede.")

    # ---------------------------------------------------------
    # MÉTODOS DE ZOOM E PAN
    # ---------------------------------------------------------
    def on_scroll(self, event):
        if not event.inaxes:
            return
        
        scale_factor = 1.1
        if event.button == 'up':
            self.zoom_level *= scale_factor
        elif event.button == 'down':
            self.zoom_level /= scale_factor
        
        # Limitar zoom
        self.zoom_level = max(0.1, min(5.0, self.zoom_level))
        
        self.desenhar_grafo()

    def on_pan_start(self, event):
        if event.inaxes and event.button == 1 and not self.modo_edicao:
            self.pan_start = (event.xdata, event.ydata)

    def on_pan(self, event):
        if self.pan_start and event.inaxes and event.button == 1 and not self.modo_edicao:
            dx = event.xdata - self.pan_start[0]
            dy = event.ydata - self.pan_start[1]
            
            # Ajustar posições dos nós
            for node in self.posicoes:
                x, y = self.posicoes[node]
                self.posicoes[node] = (x - dx, y - dy)
            
            self.pan_start = (event.xdata, event.ydata)
            self.desenhar_grafo()

    def on_pan_end(self, event):
        self.pan_start = None

    def resetar_zoom(self):
        self.zoom_level = 1.0
        if self.grafo:
            self.gerar_posicoes_automaticas()
        self.desenhar_grafo()
        self.log("Zoom resetado para nível padrão")

    # ---------------------------------------------------------
    # MÉTODOS DE EDIÇÃO CORRIGIDOS
    # ---------------------------------------------------------
    def ativar_edicao(self):
        self.modo_edicao = True
        self.log("Modo de edição ATIVADO - Arraste os nós para reposicionar")
        self.desenhar_grafo()

    def desativar_edicao(self):
        self.modo_edicao = False
        self.node_arrastando = None
        self.log("Modo de edição DESATIVADO")
        self.desenhar_grafo()

    def on_click(self, event):
        if not event.inaxes or not self.grafo:
            return

        if self.modo_edicao:
            # Encontrar o nó mais próximo do clique
            min_dist = float('inf')
            node_clicado = None
            
            for node, (x, y) in self.posicoes.items():
                dist = ((event.xdata - x) ** 2 + (event.ydata - y) ** 2) ** 0.5
                if dist < min_dist and dist < 0.1:  # Limite de distância
                    min_dist = dist
                    node_clicado = node

            if node_clicado:
                self.node_arrastando = node_clicado
                self.log(f"Selecionado nó: {node_clicado}")

    def on_motion(self, event):
        if not event.inaxes:
            return

        if self.modo_edicao and self.node_arrastando:
            # Atualizar posição do nó
            self.posicoes[self.node_arrastando] = (event.xdata, event.ydata)
            self.desenhar_grafo()

    def on_release(self, event):
        if self.node_arrastando:
            self.log(f"Nó {self.node_arrastando} reposicionado")
            self.node_arrastando = None

    def salvar_posicoes_nodes(self):
        if not self.grafo:
            messagebox.showwarning("Aviso", "Nenhum grafo carregado.")
            return
        
        try:
            salvar_posicoes(self.posicoes, "posicoes_nodes.json")
            self.log("Posições salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar posições: {str(e)}")

    def carregar_posicoes_salvas(self):
        posicoes = carregar_posicoes("posicoes_nodes.json")
        if posicoes:
            self.posicoes = posicoes
            self.log("Posições carregadas do arquivo")
            return True
        return False

    def gerar_posicoes_automaticas(self):
        """Gera posições automáticas para os nós"""
        if not self.grafo:
            return
            
        G = nx.Graph()
        for no, vizinhos in self.grafo.items():
            for viz, dist, tempo in vizinhos:
                G.add_edge(no, viz)
        
        # Usar layout de mola com parâmetros que evitam sobreposição
        self.posicoes = nx.spring_layout(G, k=3, iterations=100, seed=42)
        self.log("Posições automáticas geradas")

    # ---------------------------------------------------------
    # MÉTODOS DE ARQUIVO
    # ---------------------------------------------------------
    def atualizar_lista_arquivos(self):
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        arquivos_txt = [f for f in os.listdir(pasta_atual) if f.lower().endswith(".txt")]
        self.file_combo['values'] = arquivos_txt
        if arquivos_txt:
            self.file_combo.set(arquivos_txt[0])
            self.carregar_arquivo()

    def carregar_arquivo(self, event=None):
        arquivo = self.file_var.get()
        if not arquivo:
            return

        try:
            caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), arquivo)
            self.grafo, self.nos = ler_grafo(caminho)
            
            self.log(f"Rede carregada: {arquivo}")
            self.log(f"Total de cidades: {len(self.nos)}")
            self.log(f"Exemplo de dados: {list(self.grafo.items())[0] if self.grafo else 'N/A'}")

            # Atualizar comboboxes
            self.start_combo['values'] = self.nos
            self.end_combo['values'] = self.nos
            if self.nos:
                self.start_combo.set(self.nos[0])
                self.end_combo.set(self.nos[-1] if len(self.nos) > 1 else self.nos[0])

            # Gerar/recuperar posições
            if not self.carregar_posicoes_salvas():
                self.gerar_posicoes_automaticas()

            self.limpar_caminhos()
            self.desenhar_grafo()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")
            self.log(f"ERRO: {str(e)}")
            import traceback
            self.log(f"Detalhes: {traceback.format_exc()}")

    # ---------------------------------------------------------
    # MÉTODOS DE BUSCA CORRIGIDOS
    # ---------------------------------------------------------
    def executar_busca_principal(self):
        if not self.grafo:
            messagebox.showwarning("Aviso", "Nenhuma rede carregada.")
            return

        inicio = self.start_var.get()
        fim = self.end_var.get()

        if not inicio or not fim or inicio not in self.nos or fim not in self.nos:
            messagebox.showwarning("Aviso", "Selecione origem e destino válidos.")
            return

        try:
            self.log(f"Calculando rota: {inicio} → {fim}")
            
            # Preparar dados para busca
            nos_indices = list(range(len(self.nos)))
            no_para_indice = {no: idx for idx, no in enumerate(self.nos)}
            inicio_idx = no_para_indice[inicio]
            fim_idx = no_para_indice[fim]
            
            # Converter grafo para formato de lista
            grafo_lista = [[] for _ in range(len(self.nos))]
            for no, vizinhos in self.grafo.items():
                idx_no = no_para_indice[no]
                for viz, dist, tempo in vizinhos:
                    idx_viz = no_para_indice[viz]
                    grafo_lista[idx_no].append([idx_viz, dist, tempo])

            # Executar busca
            caminho, distancia, tempo = self.busca_obj.a_estrela_corrigido(
                inicio_idx, fim_idx, nos_indices, grafo_lista
            )

            if caminho:
                # Converter índices de volta para nomes dos nós
                indice_para_no = {idx: no for no, idx in no_para_indice.items()}
                self.caminho_ida = [indice_para_no[idx] for idx in caminho]
                
                self.log("✓ Rota encontrada!")
                self.log(f"  Caminho: {' → '.join(self.caminho_ida)}")
                self.log(f"  Distância: {distancia} km")
                self.log(f"  Tempo: {tempo} min")
                
                # Analisar congestionamento
                self.analisar_congestionamento()
            else:
                self.log("✗ Nenhuma rota encontrada!")
                self.caminho_ida = []

            self.desenhar_grafo()

        except Exception as e:
            self.log(f"ERRO no cálculo: {str(e)}")
            import traceback
            self.log(f"Detalhes: {traceback.format_exc()}")

    def executar_busca_alternativa(self):
        if not self.caminho_ida:
            messagebox.showwarning("Aviso", "Calcule a rota principal primeiro.")
            return
        
        try:
            inicio = self.start_var.get()
            fim = self.end_var.get()
            
            self.log(f"Buscando rota alternativa: {inicio} → {fim}")
            
            # Preparar dados para busca
            nos_indices = list(range(len(self.nos)))
            no_para_indice = {no: idx for idx, no in enumerate(self.nos)}
            inicio_idx = no_para_indice[inicio]
            fim_idx = no_para_indice[fim]
            
            # Converter grafo para formato de lista
            grafo_lista = [[] for _ in range(len(self.nos))]
            for no, vizinhos in self.grafo.items():
                idx_no = no_para_indice[no]
                for viz, dist, tempo in vizinhos:
                    idx_viz = no_para_indice[viz]
                    grafo_lista[idx_no].append([idx_viz, dist, tempo])
            
            # Converter caminho principal para índices
            caminho_principal_indices = [no_para_indice[no] for no in self.caminho_ida]
            
            # Executar busca por rota alternativa
            caminho_alt, distancia_alt, tempo_alt = self.busca_obj.rota_alternativa_corrigida(
                caminho_principal_indices, inicio_idx, fim_idx, nos_indices, grafo_lista
            )
            
            if caminho_alt:
                # Converter índices de volta para nomes dos nós
                indice_para_no = {idx: no for no, idx in no_para_indice.items()}
                self.caminho_alternativo = [indice_para_no[idx] for idx in caminho_alt]
                
                self.log("✓ Rota alternativa encontrada!")
                self.log(f"  Caminho alternativo: {' → '.join(self.caminho_alternativo)}")
                self.log(f"  Distância alternativa: {distancia_alt} km")
                self.log(f"  Tempo alternativo: {tempo_alt} min")
                
                # CORREÇÃO: Calcular tempo da rota principal corretamente
                tempo_principal = 0
                for i in range(len(self.caminho_ida) - 1):
                    origem = self.caminho_ida[i]
                    destino = self.caminho_ida[i + 1]
                    for viz, dist, tempo_val in self.grafo[origem]:
                        if viz == destino:
                            tempo_principal += tempo_val
                            break
                
                # CORREÇÃO: Calcular diferença corretamente
                diferenca_tempo = tempo_alt - tempo_principal
                
                if diferenca_tempo < 0:
                    # Rota alternativa é mais rápida
                    self.log(f"🎉 Rota alternativa é {abs(diferenca_tempo)}min mais rápida!")
                elif diferenca_tempo > 0:
                    # Rota alternativa é mais lenta
                    self.log(f"⚠️ Rota alternativa evita congestionamentos (mais {diferenca_tempo}min)")
                else:
                    # Mesmo tempo
                    self.log("ℹ️  Ambas as rotas têm o mesmo tempo de viagem")
                    
            else:
                self.log("✗ Nenhuma rota alternativa encontrada!")
                self.caminho_alternativo = []

            self.desenhar_grafo()

        except Exception as e:
            self.log(f"ERRO na busca alternativa: {str(e)}")
            import traceback
            self.log(f"Detalhes: {traceback.format_exc()}")

    def analisar_congestionamento(self):
        """Analisa o nível de congestionamento na rota"""
        if not self.caminho_ida:
            return
            
        self.log("Análise de congestionamento:")
        for i in range(len(self.caminho_ida) - 1):
            origem = self.caminho_ida[i]
            destino = self.caminho_ida[i + 1]
            
            # Encontrar dados da aresta
            for viz, dist, tempo in self.grafo[origem]:
                if viz == destino:
                    if dist > 0:
                        congestionamento = tempo / dist
                        nivel = "Leve" if congestionamento < 1.5 else "Moderado" if congestionamento < 2.5 else "Severo"
                        self.log(f"  {origem}→{destino}: {nivel} (tempo: {tempo}min, dist: {dist}km)")
                    break

    # ---------------------------------------------------------
    # MÉTODO DE DESENHO COM LEGENDAS COMPLETAS E ZOOM
    # ---------------------------------------------------------
    def desenhar_grafo(self):
        if not self.grafo or not self.posicoes:
            # Desenhar mensagem de erro se não houver dados
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Nenhum grafo carregado\nou posições não definidas", 
                        ha='center', va='center', transform=self.ax.transAxes, color='white', fontsize=12)
            self.ax.set_facecolor("#1e3d59")
            self.ax.axis('off')
            self.canvas.draw()
            return

        self.ax.clear()
        G = nx.Graph()

        # Adicionar nós e arestas
        for no in self.nos:
            G.add_node(no)
        
        for no, vizinhos in self.grafo.items():
            for viz, dist, tempo in vizinhos:
                G.add_edge(no, viz, weight=dist, tempo=tempo)

        # Aplicar zoom às posições
        pos_zoom = {}
        center_x = sum(x for x, y in self.posicoes.values()) / len(self.posicoes)
        center_y = sum(y for x, y in self.posicoes.values()) / len(self.posicoes)
        
        for node, (x, y) in self.posicoes.items():
            # Aplicar zoom relativo ao centro
            new_x = center_x + (x - center_x) * self.zoom_level
            new_y = center_y + (y - center_y) * self.zoom_level
            pos_zoom[node] = (new_x, new_y)

        # Configurar cores dos nós
        node_colors = []
        node_sizes = []
        
        inicio = self.start_var.get()
        fim = self.end_var.get()

        for node in G.nodes():
            if node == inicio:
                node_colors.append("#ff6b35")  # Laranja - origem
                node_sizes.append(500)
            elif node == fim:
                node_colors.append("#e74c3c")  # Vermelho - destino
                node_sizes.append(500)
            elif node in self.caminho_ida:
                node_colors.append("#9b59b6")  # Verde - rota principal"
                node_sizes.append(400)
            elif node in self.caminho_alternativo:
                node_colors.append("#f39c12")  # Laranja - rota alternativa
                node_sizes.append(400)
            else:
                node_colors.append("#3498db")  # Azul - outros
                node_sizes.append(300)

        # Desenhar arestas
        edge_colors = []
        edge_widths = []
        edge_styles = []
        
        for u, v, data in G.edges(data=True):
            # Calcular nível de congestionamento
            tempo = data.get('tempo', 1)
            dist = data.get('weight', 1)
            congestionamento = tempo / dist if dist > 0 else 1
            
            if congestionamento < 1.5:
                cor = "#27ae60"  # Verde - fluido
                largura = 1.5
            elif congestionamento < 2.5:
                cor = "#f39c12"  # Laranja - moderado
                largura = 2.5
            else:
                cor = "#e74c3c"  # Vermelho - congestionado
                largura = 3.5
                
            # Verificar se está em alguma rota
            in_principal = any(
                (self.caminho_ida[i] == u and self.caminho_ida[i + 1] == v) or
                (self.caminho_ida[i] == v and self.caminho_ida[i + 1] == u)
                for i in range(len(self.caminho_ida) - 1)
            ) if self.caminho_ida else False

            in_alternativa = any(
                (self.caminho_alternativo[i] == u and self.caminho_alternativo[i + 1] == v) or
                (self.caminho_alternativo[i] == v and self.caminho_alternativo[i + 1] == u)
                for i in range(len(self.caminho_alternativo) - 1)
            ) if self.caminho_alternativo else False

            if in_principal:
                largura = 4.0
                estilo = 'solid'
                cor = "#9b59b6"  # Roxo para rota principal
            elif in_alternativa:
                largura = 3.0
                estilo = 'dashed'
                cor = "#f39c12"  # Laranja para rota alternativa
            else:
                estilo = 'solid'
                
            edge_colors.append(cor)
            edge_widths.append(largura)
            edge_styles.append(estilo)

        # Desenhar o grafo
        nx.draw_networkx_edges(G, pos_zoom, edge_color=edge_colors, width=edge_widths, 
                              style=edge_styles, ax=self.ax, alpha=0.7)
        nx.draw_networkx_nodes(G, pos_zoom, node_color=node_colors, node_size=node_sizes,
                              ax=self.ax, edgecolors="white", linewidths=2)
        nx.draw_networkx_labels(G, pos_zoom, font_size=8, font_weight="bold", 
                               ax=self.ax, font_color="white")

        # Adicionar labels nas arestas (apenas se não for muito poluído)
        if len(G.edges()) < 50 and self.zoom_level > 0.7:  # Limitar para grafos não muito densos
            edge_labels = {}
            for u, v, data in G.edges(data=True):
                dist = data.get('weight', 1)
                tempo = data.get('tempo', 1)
                edge_labels[(u, v)] = f"{dist}km/{tempo}min"
                
            nx.draw_networkx_edge_labels(G, pos_zoom, edge_labels=edge_labels, font_size=6, 
                                       ax=self.ax, font_color="yellow")

        # =========================================================
        # LEGENDAS COMPLETAS (30% menores)
        # =========================================================
        
        # Criar patches para a legenda
        legend_patches = []
        
        # Legenda para NÓS
        legend_patches.extend([
            mpatches.Patch(color='#ff6b35', label='Armazem'),
            mpatches.Patch(color='#e74c3c', label='Ponto de Entrega'),
            mpatches.Patch(color='#9b59b6', label='Rota Principal'),
            mpatches.Patch(color='#f39c12', label='Rota Alternativa'),
            mpatches.Patch(color='#3498db', label='Ruas'),
        ])
        
        # Legenda para CONGESTIONAMENTO
        legend_patches.extend([
            mpatches.Patch(color='#27ae60', label='Fluido (cong.<1.5)'),
            mpatches.Patch(color='#f39c12', label='Moderado (1.5-2.5)'),
            mpatches.Patch(color='#e74c3c', label='Congestionado (>2.5)'),
        ])
        
        # Adicionar estatísticas se houver rota calculada
        if self.caminho_ida:
            total_distancia = 0
            total_tempo = 0
            for i in range(len(self.caminho_ida) - 1):
                origem = self.caminho_ida[i]
                destino = self.caminho_ida[i + 1]
                for viz, dist, tempo in self.grafo[origem]:
                    if viz == destino:
                        total_distancia += dist
                        total_tempo += tempo
                        break
            
            legend_patches.extend([
                mpatches.Patch(color='none', label=f'Dist: {total_distancia}km'),
                mpatches.Patch(color='none', label=f'Tempo: {total_tempo}min'),
                mpatches.Patch(color='none', label=f'Ruas: {len(self.caminho_ida)}'),
            ])

        # Adicionar legenda ao gráfico com fonte 30% menor
        legend = self.ax.legend(
            handles=legend_patches,
            loc='upper left',
            bbox_to_anchor=(0, 1),
            fontsize=7,  
            frameon=True,
            facecolor='#2a4b6e',
            edgecolor='white',
            labelcolor='white',
            ncol=2
        )
        
        # Ajustar a transparência da legenda
        legend.get_frame().set_alpha(0.9)

        # Indicador de modo de edição e zoom
        info_text = ""
        if self.modo_edicao:
            info_text += "MODO EDIÇÃO ATIVADO\n"
        if abs(self.zoom_level - 1.0) > 0.1:
            info_text += f"Zoom: {self.zoom_level:.1f}x\n"
        if info_text:
            self.ax.text(0.02, 0.02, info_text.strip(), 
                        transform=self.ax.transAxes, color="#ff6b35", fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="#1e3d59", edgecolor="#ff6b35", alpha=0.9))

        # Título do gráfico
        titulo = "Mapa de Rotas - Sistema de Logística"
        if self.caminho_ida:
            titulo += f"\n{self.start_var.get()} → {self.end_var.get()}"
        
        self.ax.set_title(titulo, color="white", fontsize=10, pad=15)  # Fonte reduzida
        self.ax.axis('off')
        self.ax.set_facecolor("#1e3d59")
        
        self.fig.tight_layout()
        self.canvas.draw()

    # ---------------------------------------------------------
    # MÉTODOS AUXILIARES
    # ---------------------------------------------------------
    def limpar_caminhos(self):
        self.caminho_ida = []
        self.caminho_alternativo = []
        self.desenhar_grafo()
        self.log("Rotas limpas")

    def log(self, mensagem):
        if self.console_text:
            self.console_text.insert(tk.END, f"{mensagem}\n")
            self.console_text.see(tk.END)
            self.console_text.update()

# ---------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceLogisticaCongestionamento(root)
    root.mainloop()