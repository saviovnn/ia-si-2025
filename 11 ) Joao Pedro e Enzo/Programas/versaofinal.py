import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import heapq
import json
import matplotlib.patches as mpatches
import random


ARQUIVO_GRAFO = "test2.txt"  
ARQUIVO_POSICOES = "posicoes_nodes.json"  



try:
    from BuscaNP import buscaNP  
except ImportError as e:
 
    print(f"Aviso: Módulo BuscaNP não encontrado. Criando classe fallback. Erro: {e}")
    
    class buscaNP:
        def __init__(self):
            pass
            
        def sucessores_grafo2(self, ind, grafo, ordem):
            return []

# ---------------------------------------------------------
# FUNÇÃO PARA LER O GRAFO 
# ---------------------------------------------------------
def ler_grafo(caminho_arquivo):
    try:
        
        with open(caminho_arquivo, "r", encoding='utf-8') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]

        if not linhas:
            return {}, []

        grafo = {}
        nos = []

        # Detectar formato automaticamente
        primeira_linha = linhas[0]
        usar_virgulas = "," in primeira_linha
        
        if usar_virgulas:  
            for linha in linhas:
                
                dados = [d.strip() for d in linha.split(",") if d.strip()]
                if not dados:
                    continue
                    
                no = dados[0]
                nos.append(no)
                vizinhos = []
                i = 1
                
                while i < len(dados):
                    try:
                        if i + 2 < len(dados):  # 3 valores
                            viz = str(dados[i])
                            dist = int(dados[i + 1])
                            tempo = int(dados[i + 2])
                            vizinhos.append((viz, dist, tempo))
                            i += 3
                        elif i + 1 < len(dados):  # 2 valores
                            viz = str(dados[i])
                            peso = int(dados[i + 1])
                            vizinhos.append((viz, peso, peso))
                            i += 2
                        else:  # 1 valor (apenas vizinho)
                            viz = str(dados[i])
                            vizinhos.append((viz, 1, 1))
                            i += 1
                    except (ValueError, IndexError):
                        i += 1 
                        
                grafo[no] = vizinhos
        else:  
            # Para grafos básicos sem vírgulas 
            nos = primeira_linha.split()
            for i, linha in enumerate(linhas[1:]):
                if i >= len(nos):
                    break
                no = nos[i]
                grafo[no] = []
                valores = linha.split()
                j = 0
                while j < len(valores):
                    try:
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
                    except (ValueError, IndexError):
                        j += 1  

        
        nos_unicos = []
        visto = set()
        for no in nos:
            if no not in visto:
                visto.add(no)
                nos_unicos.append(no)
                
        return grafo, nos_unicos
        
    except Exception as e:
        raise Exception(f"Erro ao ler arquivo {caminho_arquivo}: {str(e)}")

# ---------------------------------------------------------
# GERADOR DE NOMES DE RUAS AUTOMÁTICOS 
# ---------------------------------------------------------
class GeradorNomesRuas:
    def __init__(self):
        # Listas de nomes para ruas
        self.prefixos = [
            "Rua", "Avenida", "Alameda", "Travessa", "Viela", "Praça", 
            "Estrada", "Rodovia", "Via", "Largo", "Beco", "Passagem"
        ]
        
        self.nomes_ruas = [
            "das Flores", "do Comércio", "Principal", "São Paulo", "Rio de Janeiro",
            "Brasil", "Paulista", "Amazonas", "Bandeirantes", "Anhanguera",
            "Imigrantes", "Castelo Branco", "Raposo Tavares", "Regente Feijó",
            "7 de Setembro", "15 de Novembro", "Independência", "República",
            "Liberdade", "Justiça", "Paz", "Esperança", "União", "Progresso",
            "Central", "Nacional", "Estadual", "Municipal", "Regional", "Local",
            "Sol", "Lua", "Estrela", "Céu", "Mar", "Rio", "Montanha", "Vale",
            "Primavera", "Verão", "Outono", "Inverno", "Natureza", "Ecológica"
        ]
        
        self.nomes_personalidades = [
            "Santos Dumont", "Tiradentes", "Dom Pedro", "Princesa Isabel",
            "Getúlio Vargas", "Juscelino Kubitschek", "Tancredo Neves",
            "Duque de Caxias", "Marechal Deodoro", "Barão do Rio Branco"
        ]
        
        self.ruas_geradas = {}
        
    def gerar_nome_rua(self, no_origem, no_destino):
        """Gera um nome único para cada aresta baseado nos nós conectados"""
        chave = tuple(sorted([str(no_origem), str(no_destino)]))  # Garantir string
        
        if chave in self.ruas_geradas:
            return self.ruas_geradas[chave]
        
      
        hash_valor = hash(chave) % 1000
        
        
        if hash_valor < 400:
            prefixo = self.prefixos[hash_valor % len(self.prefixos)]
            nome_rua = self.nomes_ruas[(hash_valor // 10) % len(self.nomes_ruas)]
            nome_completo = f"{prefixo} {nome_rua}"
        elif hash_valor < 700:
            prefixo = self.prefixos[hash_valor % len(self.prefixos)]
            personalidade = self.nomes_personalidades[(hash_valor // 20) % len(self.nomes_personalidades)]
            nome_completo = f"{prefixo} {personalidade}"
        else:
            prefixo = self.prefixos[hash_valor % len(self.prefixos)]
            numero = (hash_valor % 50) + 1
            nome_completo = f"{prefixo} {numero} de Março" if random.random() > 0.5 else f"{prefixo} {numero}"
        
        self.ruas_geradas[chave] = nome_completo
        return nome_completo
    
    def obter_nome_rua(self, no_origem, no_destino):
        """Obtém o nome da rua para uma aresta específica"""
        chave = tuple(sorted([str(no_origem), str(no_destino)]))
        return self.ruas_geradas.get(chave, f"Rua {no_origem}-{no_destino}")

# ---------------------------------------------------------
# FUNÇÕES PARA SALVAR E CARREGAR POSIÇÕES 
# ---------------------------------------------------------
def salvar_posicoes(posicoes, arquivo_posicoes):
    
    try:
        posicoes_serializaveis = {}
        for node, pos in posicoes.items():
            # Converter para tipos nativos do Python compatíveis com JSON
            if hasattr(pos, 'tolist'):  # Para numpy arrays
                pos_list = pos.tolist()
            elif isinstance(pos, (tuple, list)) and len(pos) >= 2:
                # Garantir que são floats serializáveis
                pos_list = [float(pos[0]), float(pos[1])]
            else:
                continue  # Pular tipos inválidos
                
            # Garantir que a chave é string 
            posicoes_serializaveis[str(node)] = pos_list
        
        # Garantir que o diretório existe
        diretorio = os.path.dirname(arquivo_posicoes)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)
        
        
        with open(arquivo_posicoes, 'w', encoding='utf-8') as f:
            json.dump(posicoes_serializaveis, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"Posições salvas em: {arquivo_posicoes}")  # DEBUG
        return True
        
    except Exception as e:
        print(f"Erro ao salvar posições: {e}")
        return False

def carregar_posicoes(arquivo_posicoes):
  
    try:
        if not os.path.exists(arquivo_posicoes):
            print(f"Arquivo não encontrado: {arquivo_posicoes}")  
            return None
            
       
        encodings = ['utf-8', 'latin-1', 'iso-8859-1']
        posicoes_carregadas = None
        
        for encoding in encodings:
            try:
                with open(arquivo_posicoes, 'r', encoding=encoding) as f:
                    posicoes_carregadas = json.load(f)
                print(f"Arquivo carregado com encoding: {encoding}") 
                break
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                print(f"Falha com encoding {encoding}: {e}")
                continue
        
        if posicoes_carregadas is None:
            print("Não foi possível carregar o arquivo com nenhum encoding")
            return None
        
        
        posicoes = {}
        for node, pos in posicoes_carregadas.items():
            if isinstance(pos, list) and len(pos) >= 2:
                try:
                    # Garantir que as coordenadas são floats
                    x = float(pos[0]) if pos[0] is not None else 0.0
                    y = float(pos[1]) if pos[1] is not None else 0.0
                    posicoes[str(node)] = (x, y)  # Garantir chave como string
                except (ValueError, TypeError) as e:
                    print(f"Erro ao converter posição para nó {node}: {pos} - {e}")
                    continue
        
        print(f"Posições carregadas: {len(posicoes)} nós") 
        return posicoes if posicoes else None
        
    except Exception as e:
        print(f"Erro ao carregar posições: {e}")
        return None

# ---------------------------------------------------------
# CLASSE BUSCA NP CORRIGIDA PARA LINUX
# ---------------------------------------------------------
class BuscaNPCorrigida(buscaNP):
    def __init__(self):
        super().__init__()
        self.heuristicaS = {}
    
    def sucessores_grafo2_corrigido(self, ind, grafo, ordem):
      
        f = []
        for suc in grafo[ind][::ordem]:
            if isinstance(suc, (list, tuple)) and len(suc) >= 3:
                try:
                    vizinho_idx = int(suc[0])
                    dist = int(suc[1])
                    tempo = int(suc[2])
                    f.append((vizinho_idx, dist, tempo))
                except (ValueError, TypeError):
                    continue
        return f

    def heuristica(self, nos, grafo, destino_idx):
        
        if destino_idx in self.heuristicaS:
            return self.heuristicaS[destino_idx]
        
        dist = {idx: float("inf") for idx in range(len(nos))}
        dist[destino_idx] = 0
        fila = [(0, destino_idx)]
        
        while fila:
            custo_atual, atual_idx = heapq.heappop(fila)
            if custo_atual > dist[atual_idx]:
                continue
            
            for vizinho_data in grafo[atual_idx]:
                if len(vizinho_data) >= 2:
                    try:
                        vizinho_idx = int(vizinho_data[0])
                        peso = int(vizinho_data[1])
                        novo_custo = custo_atual + peso
                        if novo_custo < dist[vizinho_idx]:
                            dist[vizinho_idx] = novo_custo
                            heapq.heappush(fila, (novo_custo, vizinho_idx))
                    except (ValueError, TypeError):
                        continue
        
        self.heuristicaS[destino_idx] = dist
        return dist
    
    def heuristica_grafo(self, nos, n_idx, destino_idx, grafo):
        heuristicas = self.heuristica(nos, grafo, destino_idx)
        return heuristicas.get(n_idx, float("inf"))

    def a_estrela_corrigido(self, inicio, fim, nos, grafo, MostrarRotas=True):
        if inicio == fim:
            return [inicio], 0, 0

        lista = []
        h_inicio = self.heuristica_grafo(nos, inicio, fim, grafo)
        # Agora armazenamos tanto g_dist (distância) quanto g_tempo (tempo)
        raiz = (h_inicio, inicio, 0, 0, h_inicio, [inicio])  # (f, atual, g_dist, g_tempo, h, caminho)
        heapq.heappush(lista, raiz)
        
        visitado = set()

        while lista:
            f, atual, g_dist, g_tempo, h, caminho = heapq.heappop(lista)
            
            if atual in visitado:
                continue
                
            visitado.add(atual)

            if atual == fim:
                return caminho, g_dist, g_tempo    

            for vizinho, dist, tempo in self.sucessores_grafo2_corrigido(atual, grafo, 1):
                if vizinho in visitado:
                    continue
                    
                novo_g_dist = g_dist + dist
                novo_g_tempo = g_tempo + tempo
                novo_caminho = caminho + [vizinho]
                novo_h = self.heuristica_grafo(nos, vizinho, fim, grafo)
                novo_f = novo_g_dist + novo_h  # A heurística é baseada na distância
                
                heapq.heappush(lista, (novo_f, vizinho, novo_g_dist, novo_g_tempo, novo_h, novo_caminho))

        return None, float("inf"), float("inf")

    def rota_alternativa_corrigida(self, caminho_principal, inicio, fim, nos, grafo):
        # 1. Verificação básica do caminho
        if len(caminho_principal) < 2:
            return None, float("inf"), float("inf")

        max_congestionamento = 0
        aresta_remover = None

        # 2. Encontrar a aresta mais congestionada no caminho principal
        for i in range(len(caminho_principal) - 1):
            origem = caminho_principal[i]
            destino = caminho_principal[i + 1]

            # procura a aresta correta
            for viz, dist, tempo in grafo[origem]:
                if viz == destino and dist > 0:
                    congestionamento = tempo / dist
                    if congestionamento > max_congestionamento:
                        max_congestionamento = congestionamento
                        aresta_remover = (origem, destino)
                    break

        # Não encontrou nada
        if not aresta_remover:
            return None, float("inf"), float("inf")

        origem_idx, destino_idx = aresta_remover

        # 3. Criar cópia limpa do grafo
        grafo_temp = [list(lista) for lista in grafo]

        # 4. Remover APENAS a aresta mais congestionada (ida e volta)
        # Remove origem -> destino
        grafo_temp[origem_idx] = [
            (v, d, t) for (v, d, t) in grafo_temp[origem_idx]
            if v != destino_idx
        ]

        # Remove destino -> origem
        grafo_temp[destino_idx] = [
            (v, d, t) for (v, d, t) in grafo_temp[destino_idx]
            if v != origem_idx
        ]

        # 5. Rodar A* novamente sem essa aresta
        return self.a_estrela_corrigido(inicio, fim, nos, grafo_temp)

# ---------------------------------------------------------
# CLASSE PRINCIPAL DA INTERFACE - COMPATÍVEL COM LINUX
# ---------------------------------------------------------
class InterfaceLogisticaCongestionamento:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Logística - Roteirização com Congestionamento")
        self.root.geometry("1400x900")

        
        self.root.configure(bg="#1e3d59")
        
      
        try:
            style = ttk.Style()
            style.theme_use("clam")
        except Exception:
           
            try:
                style = ttk.Style()
                available_themes = style.theme_names()
                if 'clam' in available_themes:
                    style.theme_use("clam")
                elif 'default' in available_themes:
                    style.theme_use("default")
            except Exception:
                pass  # Usar estilo padrão

        # Cores
        azul_escuro = "#1e3d59"
        azul_medio = "#2a4b6e"
        laranja_logistica = "#ff6b35"
        verde_sucesso = "#4caf50"
        texto_branco = "#ffffff"

       
        try:
            style.configure("TFrame", background=azul_escuro)
            style.configure("TLabel", background=azul_escuro, foreground=texto_branco, font=("Arial", 10))
            style.configure("Title.TLabel", background=azul_escuro, foreground=texto_branco, font=("Arial", 12, "bold"))
            style.configure("TLabelframe", background=azul_medio, foreground=texto_branco)
            style.configure("TButton", background=laranja_logistica, foreground=texto_branco, font=("Arial", 10))
            style.map("TButton", background=[("active", "#ff8c5a")])
            style.configure("Success.TButton", background=verde_sucesso)
            style.map("Success.TButton", background=[("active", "#6bc76b")])
        except Exception as e:
            print(f"Aviso de estilo: {e}")

        # Variáveis de estado
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
        self.gerador_ruas = GeradorNomesRuas()
        self.nomes_ruas = {}
        self.console_visible = True
        self.distancia_alternativa = 0
        self.tempo_alternativa = 0

        # Variáveis de controle
        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()
        self.method_var = tk.StringVar(value="A* (Tempo)")

        self.criar_interface()
        self.carregar_arquivo_por_atributo()

    def carregar_arquivo_por_atributo(self):
      
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(ARQUIVO_GRAFO):
                
                pasta_atual = os.path.dirname(os.path.abspath(__file__))
                caminho_alternativo = os.path.join(pasta_atual, ARQUIVO_GRAFO)
                
                if os.path.exists(caminho_alternativo):
                    caminho_carregar = caminho_alternativo
                    self.log(f"Arquivo encontrado no diretório atual: {caminho_alternativo}")
                else:
                    self.log(f"ERRO: Arquivo '{ARQUIVO_GRAFO}' não encontrado!")
                    self.log("Verifique se:")
                    self.log(f"1. O arquivo '{ARQUIVO_GRAFO}' está no mesmo diretório do script")
                    self.log(f"2. Ou altere a variável ARQUIVO_GRAFO no código")
                    messagebox.showerror("Erro", f"Arquivo '{ARQUIVO_GRAFO}' não encontrado!\n\nVerifique se o arquivo está no diretório correto.")
                    return
            else:
                caminho_carregar = ARQUIVO_GRAFO
            
            self.log(f"Carregando arquivo: {caminho_carregar}")
            self.grafo, self.nos = ler_grafo(caminho_carregar)
            
            if not self.grafo or not self.nos:
                self.log("ERRO: Arquivo vazio ou formato inválido!")
                messagebox.showerror("Erro", "Arquivo vazio ou formato inválido!")
                return
            
            self.gerar_nomes_ruas_automaticos()
            
            self.log(f"✓ Rede carregada com sucesso: {os.path.basename(caminho_carregar)}")
            self.log(f"  Total de cidades: {len(self.nos)}")
            self.log(f"  Nomes de ruas gerados: {len(self.nomes_ruas)} arestas")

            # Atualizar comboboxes
            self.start_combo['values'] = self.nos
            self.end_combo['values'] = self.nos
            if self.nos:
                self.start_combo.set(self.nos[0])
                if len(self.nos) > 1:
                    self.end_combo.set(self.nos[-1])

            # Gerar/recuperar posições
            if not self.carregar_posicoes_por_atributo():
                self.gerar_posicoes_automaticas()

            self.limpar_caminhos()
            self.desenhar_grafo()
            
        except Exception as e:
            error_msg = f"Erro ao carregar arquivo '{ARQUIVO_GRAFO}': {str(e)}"
            self.log(f"ERRO: {error_msg}")
            messagebox.showerror("Erro", error_msg)

    def carregar_posicoes_por_atributo(self):
        """Carrega as posições do arquivo JSON definido no atributo ARQUIVO_POSICOES"""
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(ARQUIVO_POSICOES):
                # Tentar encontrar o arquivo no diretório atual
                pasta_atual = os.path.dirname(os.path.abspath(__file__))
                caminho_alternativo = os.path.join(pasta_atual, ARQUIVO_POSICOES)
                
                if os.path.exists(caminho_alternativo):
                    caminho_carregar = caminho_alternativo
                    self.log(f"Arquivo de posições encontrado no diretório atual: {caminho_alternativo}")
                else:
                    self.log(f"Arquivo de posições '{ARQUIVO_POSICOES}' não encontrado. Gerando posições automáticas.")
                    return False
            else:
                caminho_carregar = ARQUIVO_POSICOES
            
            self.log(f"Carregando posições: {caminho_carregar}")
            posicoes = carregar_posicoes(caminho_carregar)
            
            if posicoes:
                # Verificar se temos posições para todos os nós atuais
                nos_faltantes = [no for no in self.nos if no not in posicoes]
                if not nos_faltantes:
                    self.posicoes = posicoes
                    self.log(f"✓ Posições carregadas do arquivo: {caminho_carregar}")
                    self.log(f"  Total de posições carregadas: {len(posicoes)}")
                    return True
                else:
                    self.log(f"Arquivo de posições incompleto. Nós faltantes: {len(nos_faltantes)}")
                    # Mesclar posições existentes com posições aleatórias para nós faltantes
                    for no in nos_faltantes:
                        posicoes[no] = (random.uniform(-1, 1), random.uniform(-1, 1))
                    self.posicoes = posicoes
                    self.log("✓ Posições mescladas com sucesso")
                    return True
            else:
                self.log("✗ Falha ao carregar posições do arquivo")
                return False
                
        except Exception as e:
            self.log(f"Erro ao carregar posições salvas: {e}")
            return False

    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Logística - Roteirização com Congestionamento", 
                               style="Title.TLabel" if hasattr(ttk, 'Style') else None)
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

        # Informação dos arquivos carregados
        ttk.Label(route_config_frame, text="Arquivos Carregados:").pack(anchor=tk.W)
        info_label = ttk.Label(route_config_frame, text=f"Grafo: {ARQUIVO_GRAFO} | Posições: {ARQUIVO_POSICOES}", 
                              foreground="#ff6b35", font=("Arial", 9))
        info_label.pack(anchor=tk.W, pady=(5, 10))
        self.info_label = info_label

        # Origem e Destino
        ttk.Label(route_config_frame, text="Ponto de Partida:").pack(anchor=tk.W)
        self.start_combo = ttk.Combobox(route_config_frame, textvariable=self.start_var)
        self.start_combo.pack(fill=tk.X, pady=(5, 10))

        ttk.Label(route_config_frame, text="Ponto de Entrega:").pack(anchor=tk.W)
        self.end_combo = ttk.Combobox(route_config_frame, textvariable=self.end_var)
        self.end_combo.pack(fill=tk.X, pady=(5, 10))

        # Botões de busca
        ttk.Button(route_config_frame, text="Calcular Rota Principal", 
                  command=self.executar_busca_principal).pack(fill=tk.X, pady=5)

        ttk.Button(route_config_frame, text="Buscar Rota Alternativa", 
                  command=self.executar_busca_alternativa).pack(fill=tk.X, pady=5)

        # Painel de informações da rota alternativa
        self.alternative_info_frame = ttk.LabelFrame(control_frame, text="Rota Alternativa", padding=10)
        self.alternative_info_frame.pack(fill=tk.X, pady=(10, 0))

        # Inicialmente vazio
        self.alternative_info_label = ttk.Label(self.alternative_info_frame, text="Nenhuma rota alternativa calculada", 
                                               foreground="#cccccc", font=("Arial", 9))
        self.alternative_info_label.pack(anchor=tk.W, pady=5)

        # Controles
        edit_frame = ttk.LabelFrame(control_frame, text="Controles", padding=10)
        edit_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(edit_frame, text="Limpar Rotas", 
                  command=self.limpar_caminhos).pack(fill=tk.X, pady=2)

        ttk.Button(edit_frame, text="Recarregar Grafo", 
                  command=self.recarregar_grafo).pack(fill=tk.X, pady=2)

        ttk.Button(edit_frame, text="Recarregar Posições", 
                  command=self.recarregar_posicoes).pack(fill=tk.X, pady=2)

       

        ttk.Button(edit_frame, text="🔽 Ocultar Log", 
                  command=self.toggle_console).pack(fill=tk.X, pady=2)

        # Console de saída
        self.console_frame = ttk.LabelFrame(control_frame, text="Log do Sistema", padding=10)
        self.console_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.console_text = scrolledtext.ScrolledText(self.console_frame, height=15, 
                                                     bg="#0d2b47", fg="white", 
                                                     font=("DejaVu Sans Mono", 9) if os.name != 'nt' else ("Consolas", 9))
        self.console_text.pack(fill=tk.BOTH, expand=True)

        # Área do gráfico - compatível com Linux
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor="#1e3d59")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1e3d59")
        
        # Backend compatível com Linux
        try:
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        except Exception as e:
            print(f"Aviso backend matplotlib: {e}")
            # Tentar fallback
            import matplotlib
            matplotlib.use('TkAgg')
            self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
            
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Conectar eventos do mouse
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("button_press_event", self.on_pan_start)
        self.canvas.mpl_connect("motion_notify_event", self.on_pan)
        self.canvas.mpl_connect("button_release_event", self.on_pan_end)

        self.log(f"Sistema iniciado. Configuração:")
        self.log(f"  Arquivo do grafo: {ARQUIVO_GRAFO}")
        self.log(f"  Arquivo de posições: {ARQUIVO_POSICOES}")

    def atualizar_info_alternativa(self):
        """Atualiza o painel de informações da rota alternativa"""
        if self.caminho_alternativo and self.distancia_alternativa > 0:
            info_text = f"Distância: {self.distancia_alternativa} km\nTempo: {self.tempo_alternativa} min"
            self.alternative_info_label.config(text=info_text, foreground="#f39c12")
        else:
            self.alternative_info_label.config(text="Nenhuma rota alternativa calculada", foreground="#cccccc")

    def recarregar_grafo(self):
        """Recarrega o arquivo de grafo definido no atributo"""
        self.log(f"Recarregando arquivo de grafo: {ARQUIVO_GRAFO}")
        self.carregar_arquivo_por_atributo()

    def recarregar_posicoes(self):
        """Recarrega o arquivo de posições definido no atributo"""
        self.log(f"Recarregando arquivo de posições: {ARQUIVO_POSICOES}")
        if self.carregar_posicoes_por_atributo():
            self.desenhar_grafo()
        else:
            self.log("Falha ao recarregar posições. Gerando posições automáticas.")
            self.gerar_posicoes_automaticas()

    def toggle_console(self):
        if self.console_visible:
            self.console_frame.pack_forget()
            self.console_visible = False
            for widget in self.console_frame.master.winfo_children():
                if isinstance(widget, ttk.Button) and "🔽" in widget.cget('text'):
                    widget.configure(text="🔼 Mostrar Log")
                    break
        else:
            self.console_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
            self.console_visible = True
            for widget in self.console_frame.master.winfo_children():
                if isinstance(widget, ttk.Button) and "🔼" in widget.cget('text'):
                    widget.configure(text="🔽 Ocultar Log")
                    break

    # ---------------------------------------------------------
    # MÉTODOS DE ZOOM E PAN
    # ---------------------------------------------------------
    def on_scroll(self, event):
        if not event.inaxes:
            return
        
        scale_factor = 1.1
        if event.button == 'up':
            self.zoom_level = min(5.0, self.zoom_level * scale_factor)
        elif event.button == 'down':
            self.zoom_level = max(0.1, self.zoom_level / scale_factor)
        
        self.desenhar_grafo()

    def on_pan_start(self, event):
        if event.inaxes and event.button == 1 and not self.modo_edicao:
            self.pan_start = (event.xdata, event.ydata)

    def on_pan(self, event):
        if self.pan_start and event.inaxes and event.button == 1 and not self.modo_edicao:
            dx = event.xdata - self.pan_start[0]
            dy = event.ydata - self.pan_start[1]
            
            self.posicoes = {node: (x - dx, y - dy) for node, (x, y) in self.posicoes.items()}
            self.pan_start = (event.xdata, event.ydata)
            self.desenhar_grafo()

    def on_pan_end(self, event):
        self.pan_start = None

    def gerar_posicoes_automaticas(self):
        """Gera posições automáticas e salva no arquivo definido no atributo"""
        if not self.grafo:
            return
            
        G = nx.Graph()
        for no, vizinhos in self.grafo.items():
            for viz, dist, tempo in vizinhos:
                G.add_edge(no, viz)
        
        # Layout compatível com Linux
        try:
            self.posicoes = nx.spring_layout(G, k=3, iterations=100, seed=42)
        except Exception:
            # Fallback para layout mais simples
            self.posicoes = nx.circular_layout(G)
            
        self.log("Posições automáticas geradas")
        
        # SALVAR AS POSIÇÕES GERADAS AUTOMATICAMENTE NO ARQUIVO DEFINIDO
        if salvar_posicoes(self.posicoes, ARQUIVO_POSICOES):
            self.log(f"✓ Posições salvas em: {ARQUIVO_POSICOES}")
        else:
            self.log("✗ Erro ao salvar posições automáticas")

    def salvar_posicoes_atuais(self):
        """Salva as posições atuais no arquivo definido no atributo"""
        if self.posicoes:
            if salvar_posicoes(self.posicoes, ARQUIVO_POSICOES):
                self.log(f"✓ Posições atuais salvas em: {ARQUIVO_POSICOES}")
                return True
            else:
                self.log("✗ Erro ao salvar posições atuais")
                return False
        else:
            self.log("ℹ️ Nenhuma posição para salvar")
            return False

    def gerar_nomes_ruas_automaticos(self):
        self.nomes_ruas = {}
        
        for no_origem, vizinhos in self.grafo.items():
            for vizinho_data in vizinhos:
                if vizinho_data:
                    no_destino = vizinho_data[0]
                    nome_rua = self.gerador_ruas.gerar_nome_rua(no_origem, no_destino)
                    chave = tuple(sorted([no_origem, no_destino]))
                    self.nomes_ruas[chave] = nome_rua

        # Atualizar label de informação
        if hasattr(self, 'info_label'):
            self.info_label.config(text=f"Grafo: {ARQUIVO_GRAFO} | Posições: {ARQUIVO_POSICOES} | {len(self.nos)} cidades, {len(self.nomes_ruas)} ruas")

    def obter_nome_rua(self, no_origem, no_destino):
        chave = tuple(sorted([no_origem, no_destino]))
        return self.nomes_ruas.get(chave, f"Rua {no_origem}-{no_destino}")

    # ---------------------------------------------------------
    # MÉTODOS DE BUSCA (mantidos iguais)
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
            
            nos_indices = list(range(len(self.nos)))
            no_para_indice = {no: idx for idx, no in enumerate(self.nos)}
            inicio_idx = no_para_indice[inicio]
            fim_idx = no_para_indice[fim]
            
            grafo_lista = [[] for _ in range(len(self.nos))]
            for no, vizinhos in self.grafo.items():
                idx_no = no_para_indice[no]
                for viz, dist, tempo in vizinhos:
                    idx_viz = no_para_indice[viz]
                    grafo_lista[idx_no].append([idx_viz, dist, tempo])

            caminho, distancia, tempo = self.busca_obj.a_estrela_corrigido(
                inicio_idx, fim_idx, nos_indices, grafo_lista
            )

            if caminho:
                indice_para_no = {idx: no for no, idx in no_para_indice.items()}
                self.caminho_ida = [indice_para_no[idx] for idx in caminho]
                
                self.log("✓ Rota encontrada!")
                self.log(f"  Caminho: {' → '.join(self.caminho_ida)}")
                self.log(f"  Distância: {distancia} km")
                self.log(f"  Tempo: {tempo} min")
                
                self.log("  Ruas na rota:")
                for i in range(len(self.caminho_ida) - 1):
                    origem = self.caminho_ida[i]
                    destino = self.caminho_ida[i + 1]
                    nome_rua = self.obter_nome_rua(origem, destino)
                    self.log(f"    - {nome_rua}")
                
                self.analisar_congestionamento()
            else:
                self.log("✗ Nenhuma rota encontrada!")
                self.caminho_ida = []

            self.desenhar_grafo()

        except Exception as e:
            self.log(f"ERRO no cálculo: {str(e)}")

    def executar_busca_alternativa(self):
        if not self.caminho_ida:
            messagebox.showwarning("Aviso", "Calcule a rota principal primeiro.")
            return
        
        try:
            inicio = self.start_var.get()
            fim = self.end_var.get()
            
            self.log(f"Buscando rota alternativa: {inicio} → {fim}")
            
            nos_indices = list(range(len(self.nos)))
            no_para_indice = {no: idx for idx, no in enumerate(self.nos)}
            inicio_idx = no_para_indice[inicio]
            fim_idx = no_para_indice[fim]
            
            grafo_lista = [[] for _ in range(len(self.nos))]
            for no, vizinhos in self.grafo.items():
                idx_no = no_para_indice[no]
                for viz, dist, tempo in vizinhos:
                    idx_viz = no_para_indice[viz]
                    grafo_lista[idx_no].append([idx_viz, dist, tempo])
            
            caminho_principal_indices = [no_para_indice[no] for no in self.caminho_ida]
            
            caminho_alt, distancia_alt, tempo_alt = self.busca_obj.rota_alternativa_corrigida(
                caminho_principal_indices, inicio_idx, fim_idx, nos_indices, grafo_lista
            )
            
            if caminho_alt:
                indice_para_no = {idx: no for no, idx in no_para_indice.items()}
                self.caminho_alternativo = [indice_para_no[idx] for idx in caminho_alt]
                self.distancia_alternativa = distancia_alt
                self.tempo_alternativa = tempo_alt
                
                self.log("✓ Rota alternativa encontrada!")
                self.log(f"  Caminho alternativo: {' → '.join(self.caminho_alternativo)}")
                self.log(f"  Distância: {distancia_alt} km")
                self.log(f"  Tempo: {tempo_alt} min")
                
                tempo_principal = sum(
                    tempo_val for i in range(len(self.caminho_ida) - 1)
                    for viz, dist, tempo_val in self.grafo[self.caminho_ida[i]]
                    if viz == self.caminho_ida[i + 1]
                )
                
                diferenca_tempo = tempo_alt - tempo_principal
                
                if diferenca_tempo < 0:
                    self.log(f"🎉 Rota alternativa é {abs(diferenca_tempo)}min mais rápida!")
                elif diferenca_tempo > 0:
                    self.log(f"⚠️ Rota alternativa evita congestionamentos (mais {diferenca_tempo}min)")
                else:
                    self.log("ℹ️  Ambas as rotas têm o mesmo tempo de viagem")
                    
                # Atualizar painel de informações
                self.atualizar_info_alternativa()
                    
            else:
                self.log("✗ Nenhuma rota alternativa encontrada!")
                self.caminho_alternativo = []
                self.distancia_alternativa = 0
                self.tempo_alternativa = 0
                self.atualizar_info_alternativa()

            self.desenhar_grafo()

        except Exception as e:
            self.log(f"ERRO na busca alternativa: {str(e)}")

    def analisar_congestionamento(self):
        if not self.caminho_ida:
            return
            
        self.log("Análise de congestionamento:")
        for i in range(len(self.caminho_ida) - 1):
            origem = self.caminho_ida[i]
            destino = self.caminho_ida[i + 1]
            
            for viz, dist, tempo in self.grafo[origem]:
                if viz == destino and dist > 0:
                    congestionamento = tempo / dist
                    nivel = "Leve" if congestionamento < 1.5 else "Moderado" if congestionamento < 2.5 else "Severo"
                    nome_rua = self.obter_nome_rua(origem, destino)
                    self.log(f"  {nome_rua}: {nivel} (tempo: {tempo}min, dist: {dist}km)")
                    break

    def desenhar_grafo(self):
        if not self.grafo or not self.posicoes:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Nenhum grafo carregado\nou posições não definidas", 
                        ha='center', va='center', transform=self.ax.transAxes, color='white', fontsize=12)
            self.ax.set_facecolor("#1e3d59")
            self.ax.axis('off')
            self.canvas.draw()
            return

        self.ax.clear()
        G = nx.Graph()

        for no in self.nos:
            G.add_node(no)
        
        for no, vizinhos in self.grafo.items():
            for viz, dist, tempo in vizinhos:
                G.add_edge(no, viz, weight=dist, tempo=tempo)

        center_x = sum(x for x, y in self.posicoes.values()) / len(self.posicoes)
        center_y = sum(y for x, y in self.posicoes.values()) / len(self.posicoes)
        
        pos_zoom = {
            node: (
                center_x + (x - center_x) * self.zoom_level,
                center_y + (y - center_y) * self.zoom_level
            )
            for node, (x, y) in self.posicoes.items()
        }

        inicio = self.start_var.get()
        fim = self.end_var.get()
        
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            if node == inicio:
                node_colors.append("#ff6b35")
                node_sizes.append(500)
            elif node == fim:
                node_colors.append("#e74c3c")
                node_sizes.append(500)
            elif node in self.caminho_ida:
                node_colors.append("#9b59b6")
                node_sizes.append(400)
            elif node in self.caminho_alternativo:
                node_colors.append("#f39c12")
                node_sizes.append(400)
            else:
                node_colors.append("#3498db")
                node_sizes.append(300)

        edge_colors = []
        edge_widths = []
        edge_styles = []
        
        for u, v, data in G.edges(data=True):
            tempo = data.get('tempo', 1)
            dist = data.get('weight', 1)
            congestionamento = tempo / dist if dist > 0 else 1
            
            if congestionamento < 1.5:
                cor = "#27ae60"
                largura = 1.5
            elif congestionamento < 2.5:
                cor = "#f39c12"
                largura = 2.5
            else:
                cor = "#e74c3c"
                largura = 3.5
                
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
                cor = "#9b59b6"
            elif in_alternativa:
                largura = 3.0
                estilo = 'dashed'
                cor = "#f39c12"
            else:
                estilo = 'solid'
                
            edge_colors.append(cor)
            edge_widths.append(largura)
            edge_styles.append(estilo)

        nx.draw_networkx_edges(G, pos_zoom, edge_color=edge_colors, width=edge_widths, 
                              style=edge_styles, ax=self.ax, alpha=0.7)
        
        nx.draw_networkx_nodes(G, pos_zoom, node_color=node_colors, node_size=node_sizes,
                              ax=self.ax, edgecolors="white", linewidths=2)
        
        nx.draw_networkx_labels(G, pos_zoom, font_size=8, font_weight="bold", 
                               ax=self.ax, font_color="white")

        edge_labels = {(u, v): self.obter_nome_rua(u, v) for u, v in G.edges()}
        
        if edge_labels:
            nx.draw_networkx_edge_labels(
                G, pos_zoom, 
                edge_labels=edge_labels,
                font_size=7,
                font_color='yellow',
                ax=self.ax,
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    facecolor="#1e3d59",
                    edgecolor="yellow",
                    alpha=0.9
                ),
                rotate=False
            )

        legend_patches = [
            mpatches.Patch(color='#ff6b35', label='Armazem'),
            mpatches.Patch(color='#e74c3c', label='Ponto de Entrega'),
            mpatches.Patch(color='#9b59b6', label='Rota Principal'),
            mpatches.Patch(color='#f39c12', label='Rota Alternativa'),
            mpatches.Patch(color='#3498db', label='Ruas'),
            mpatches.Patch(color='#27ae60', label='Fluido (cong.<1.5)'),
            mpatches.Patch(color='#f39c12', label='Moderado (1.5-2.5)'),
            mpatches.Patch(color='#e74c3c', label='Congestionado (>2.5)'),
        ]
        
        if self.caminho_ida:
            total_distancia = 0
            total_tempo = 0
            for i in range(len(self.caminho_ida) - 1):
                origem = self.caminho_ida[i]
                destino = self.caminho_ida[i + 1]
                for viz, dist, tempo_val in self.grafo[origem]:
                    if viz == destino:
                        total_distancia += dist
                        total_tempo += tempo_val
                        break
            
            legend_patches.extend([
                mpatches.Patch(color='none', label=f'Dist: {total_distancia}km'),
                mpatches.Patch(color='none', label=f'Tempo: {total_tempo}min'),
            ])

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
        legend.get_frame().set_alpha(0.9)

        if abs(self.zoom_level - 1.0) > 0.1:
            self.ax.text(0.02, 0.02, f"Zoom: {self.zoom_level:.1f}x", 
                        transform=self.ax.transAxes, color="#ff6b35", fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="#1e3d59", 
                                edgecolor="#ff6b35", alpha=0.9))

        titulo = f"Mapa de Rotas - {ARQUIVO_GRAFO}"
        if self.caminho_ida:
            titulo += f"\n{self.start_var.get()} → {self.end_var.get()}"
        
        self.ax.set_title(titulo, color="white", fontsize=10, pad=15)
        self.ax.axis('off')
        self.ax.set_facecolor("#1e3d59")
        
        self.fig.tight_layout()
        self.canvas.draw()

    def limpar_caminhos(self):
        self.caminho_ida.clear()
        self.caminho_alternativo.clear()
        self.distancia_alternativa = 0
        self.tempo_alternativa = 0
        self.atualizar_info_alternativa()
        self.desenhar_grafo()
        self.log("Rotas limpas")

    def log(self, mensagem):
        if hasattr(self, 'console_text') and self.console_text:
            self.console_text.insert(tk.END, f"{mensagem}\n")
            self.console_text.see(tk.END)
            self.console_text.update_idletasks()

# ---------------------------------------------------------
# PROGRAMA PRINCIPAL COMPATÍVEL COM LINUX
# ---------------------------------------------------------
if __name__ == "__main__":
    # Configuração prévia para Linux
    if os.name != 'nt':  # Não é Windows
        # Configurar para Linux
        import matplotlib
        matplotlib.use('TkAgg')  # Forçar backend TkAgg para Linux
        
    try:
        root = tk.Tk()
        app = InterfaceLogisticaCongestionamento(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        print("Certifique-se de que todas as dependências estão instaladas:")
        print("sudo apt-get install python3-tk python3-pip")
        print("pip install networkx matplotlib")