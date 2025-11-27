import json
from collections import defaultdict

class JsonGrafoLoader:
    def __init__(self, arquivo_grafo):
        self.arquivo_grafo = arquivo_grafo
        self.nos = []
        self.grafo = defaultdict(list)
        self.distancias = {}
        self.bitola = ""
        self.total_cidades = 0
        self.total_conexoes = 0
        self.carregar_grafo()
    
    def carregar_grafo(self):
        """Carrega o grafo a partir do arquivo JSON"""
        with open(self.arquivo_grafo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extrair metadados
        self.bitola = data.get("bitola", "")
        self.total_cidades = data.get("total_cidades", 0)
        self.total_conexoes = data.get("total_conexoes", 0)
        
        # Carregar grafo
        grafo_data = data.get("grafo", {})
        
        for cidade, conexoes in grafo_data.items():
            # Adicionar cidade à lista de nós se não existir
            if cidade not in self.nos:
                self.nos.append(cidade)
            
            # Processar conexões
            for destino, distancia in conexoes.items():
                # Adicionar destino à lista de nós se não existir
                if destino not in self.nos:
                    self.nos.append(destino)
                
                # Adicionar conexão no grafo (bidirecional)
                if destino not in self.grafo[cidade]:
                    self.grafo[cidade].append(destino)
                if cidade not in self.grafo[destino]:
                    self.grafo[destino].append(cidade)
                
                # Armazenar distância (bidirecional)
                self.distancias[(cidade, destino)] = distancia
                self.distancias[(destino, cidade)] = distancia
        
        print(f"Grafo JSON carregado: {len(self.nos)} cidades, {len(self.distancias)//2} conexões")
        print(f"Bitola: {self.bitola}")
    
    def obter_sucessores(self, cidade):
        """Retorna lista de cidades conectadas à cidade dada"""
        return self.grafo.get(cidade, [])
    
    def obter_distancia(self, cidade_a, cidade_b):
        """Retorna a distância entre duas cidades"""
        return self.distancias.get((cidade_a, cidade_b), float('inf'))
    
    def listar_cidades(self):
        """Retorna lista de todas as cidades"""
        return sorted(self.nos)
        # Usa diretamente a distância do grafo (em km)

    def verificar_cidade_existe(self, cidade):
        """Verifica se uma cidade existe no grafo"""
        return cidade in self.nos
