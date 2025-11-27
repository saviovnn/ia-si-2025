from collections import deque
import math
from Node import Node
from JsonGrafoLoader import JsonGrafoLoader

class buscaNP(object):
    def __init__(self, arquivo_grafo, use_json=True):
        self.grafo_loader = JsonGrafoLoader(arquivo_grafo)
        self.nos = self.grafo_loader.nos
    
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRAFO
    #--------------------------------------------------------------------------
    def sucessores_grafo(self, cidade, ordem=1):
        """Retorna sucessores de uma cidade no grafo"""
        sucessores = self.grafo_loader.obter_sucessores(cidade)
        if ordem == -1:
            sucessores = sucessores[::-1]  # Inverte ordem para busca em profundidade
        return sucessores
    #--------------------------------------------------------------------------    
    # HEURÍSTICA DE DISTÂNCIA
    #--------------------------------------------------------------------------
    
    def heuristica_distancia(self, cidade_atual, cidade_destino):
        """
        Calcula a heurística baseada na distância em km do grafo
        Usa a distância em linha reta já disponível nos dados
        """
        distancia = self.grafo_loader.obter_distancia(cidade_atual, cidade_destino)
        
        # Se não há conexão direta, retorna um valor alto para a heurística
        if distancia == float('inf'):
            return 1000  # Valor alto para indicar distância desconhecida
        
        return distancia
    
    #--------------------------------------------------------------------------    
    # EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
    #--------------------------------------------------------------------------    
    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
    #--------------------------------------------------------------------------    
    # CONTROLE DE NÓS REPETIDOS
    #--------------------------------------------------------------------------
    def exibirCaminho1(self,encontro,visitado1, visitado2):
        # nó do lado do início
        encontro1 = visitado1[encontro]  
        # nó do lado do objetivo
        encontro2 = visitado2[encontro]
    
        caminho1 = self.exibirCaminho(encontro1)
        caminho2 = self.exibirCaminho(encontro2)
    
        # Inverte o caminho
        caminho2 = list(reversed(caminho2[:-1]))
    
        return caminho1 + caminho2
    #--------------------------------------------------------------------------
    # BUSCA EM AMPLITUDE
    #--------------------------------------------------------------------------
    def amplitude(self, inicio, fim):
        if inicio == fim:
            return [inicio]
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        fila.append(Node(None,inicio,0,None,None))
    
        # Marca início como visitado
        visitado = {inicio: 0}
    
        while fila:
            # Remove o primeiro da FILA
            atual = fila.popleft()
    
            # Gera sucessores a partir do grafo
            filhos = self.sucessores_grafo(atual.estado, 1)
    
            for novo in filhos:
                if novo not in visitado:
                    filho = Node(atual,novo,atual.v1 + 1,None,None)
                    fila.append(filho)
                    visitado[novo] = filho.v1
    
                    # Verifica se encontrou o objetivo
                    if novo == fim:
                        return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE
    #--------------------------------------------------------------------------
    def profundidade(self, inicio, fim):
        if inicio == fim:
            return [inicio]
        # Lista para árvore de busca - PILHA
        pilha = deque()
    
        # Inclui início como nó raíz da árvore de busca
        pilha.append(Node(None,inicio,0,None,None))
    
        # Marca início como visitado
        visitado = {inicio: 0}
    
        while pilha:
            # Remove o último da PILHA
            atual = pilha.pop()
    
            # Gera sucessores a partir do grafo
            filhos = self.sucessores_grafo(atual.estado, -1)
    
            for novo in filhos:
                if novo not in visitado:
                    filho = Node(atual,novo,atual.v1 + 1,None,None)
                    pilha.append(filho)
                    visitado[novo] = filho.v1
    
                    # Verifica se encontrou o objetivo
                    if novo == fim:
                        return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE LIMITADA
    #--------------------------------------------------------------------------
    def prof_limitada(self, inicio, fim, lim):
        if inicio == fim:
            return [inicio]
        
        # Lista para árvore de busca - PILHA
        pilha = deque()
    
        # Inclui início como nó raíz da árvore de busca
        pilha.append(Node(None,inicio,0,None,None))
    
        # Marca início como visitado
        visitado = {inicio: 0}
    
        while pilha:
            # Remove o último da PILHA
            atual = pilha.pop()
            
            if atual.v1 < lim:
                # Gera sucessores a partir do grafo
                filhos = self.sucessores_grafo(atual.estado, -1)
        
                for novo in filhos:
                    if novo not in visitado:
                        filho = Node(atual,novo,atual.v1 + 1,None,None)
                        pilha.append(filho)
                        visitado[novo] = filho.v1
        
                        # Verifica se encontrou o objetivo
                        if novo == fim:
                            return self.exibirCaminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM APROFUNDAMENTO ITERATIVO
    #--------------------------------------------------------------------------
    def aprof_iterativo(self, inicio, fim, lim_max):
        if inicio == fim:
            return [inicio]
        
        for lim in range(1, lim_max + 1):
            # Lista para árvore de busca - PILHA
            pilha = deque()
        
            # Inclui início como nó raíz da árvore de busca
            pilha.append(Node(None,inicio,0,None,None))
        
            # Marca início como visitado
            visitado = {inicio: 0}
        
            while pilha:
                # Remove o último da PILHA
                atual = pilha.pop()
                
                if atual.v1 < lim:
                    # Gera sucessores a partir do grafo
                    filhos = self.sucessores_grafo(atual.estado, -1)
            
                    for novo in filhos:
                        if novo not in visitado:
                            filho = Node(atual,novo,atual.v1 + 1,None,None)
                            pilha.append(filho)
                            visitado[novo] = filho.v1
            
                            # Verifica se encontrou o objetivo
                            if novo == fim:
                                return self.exibirCaminho(filho)
            
            # Limpa estruturas para próxima iteração
            pilha.clear()
            visitado.clear()
        return None
    #--------------------------------------------------------------------------
    # BUSCA BIDIRECIONAL
    #--------------------------------------------------------------------------
    def bidirecional(self, inicio, fim):
        if inicio == fim:
            return [inicio]

        # Lista para árvore de busca a partir da origem - FILA
        fila1 = deque()
        
        # Lista para árvore de busca a partir do destino - FILA
        fila2 = deque()  
        
        # Inclui início e fim como nó raíz da árvore de busca
        fila1.append(Node(None,inicio,0,None,None))
        fila2.append(Node(None,fim,0,None,None))
    
        # Visitados mapeando estado -> Node (para reconstruir o caminho)
        visitado1 = {inicio: fila1[0]}
        visitado2 = {fim:    fila2[0]}
        
        nivel = 0
    
        while fila1 and fila2:
            
            # ****** Executa AMPLITUDE a partir da ORIGEM *******
            # Quantidade de nós no nível atual
            nivel = len(fila1)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila1.popleft()

                # Gera sucessores
                filhos = self.sucessores_grafo(atual.estado, 1)

                for novo in filhos:
                    if novo not in visitado1:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado1[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado2:
                            return self.exibirCaminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        fila1.append(filho)
            
            # ****** Executa AMPLITUDE a partir do OBJETIVO *******
            # Quantidade de nós no nível atual
            nivel = len(fila2)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila2.popleft()

                # Gera sucessores
                filhos = self.sucessores_grafo(atual.estado, 1)

                for novo in filhos:
                    if novo not in visitado2:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado2[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado1:
                            return self.exibirCaminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        fila2.append(filho)
        return None
    
    #--------------------------------------------------------------------------
    # CUSTO UNIFORME
    #--------------------------------------------------------------------------
    def custo_uniforme(self, inicio, fim):
        """
        Algoritmo de busca por custo uniforme usando distância real do grafo
        """
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em custo g(n)
        fila = []
        raiz = Node(None, inicio, 0, None, None)
        fila.append(raiz)
        
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        while fila:
            # Remove o nó com menor custo g(n)
            atual = fila.pop(0)
            
            # Chegou ao objetivo
            if atual.estado == fim:
                return self.exibirCaminho(atual)
            
            # Gera sucessores
            filhos = self.sucessores_grafo(atual.estado, 1)
            
            for novo in filhos:
                # Custo g(n) = custo do caminho até aqui
                g_novo = atual.v1 + self.grafo_loader.obter_distancia(atual.estado, novo)
                
                # Se não foi visitado ou encontrou um caminho melhor
                if novo not in visitado or g_novo < visitado[novo].v1:
                    filho = Node(atual, novo, g_novo, None, None)
                    visitado[novo] = filho
                    
                    # Insere ordenado por custo g(n)
                    self.inserir_ordenado_heuristica(fila, filho)
        
        return None
    
    #--------------------------------------------------------------------------
    # GREEDY (BUSCA GULOSA)
    #--------------------------------------------------------------------------
    def greedy(self, inicio, fim):
        """
        Algoritmo de busca gulosa usando heurística de distância
        """
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em heurística
        fila = []
        raiz = Node(None, inicio, 0, None, None)
        fila.append(raiz)
        
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        while fila:
            # Remove o nó com menor heurística (primeiro da lista ordenada)
            atual = fila.pop(0)
            
            # Chegou ao objetivo
            if atual.estado == fim:
                return self.exibirCaminho(atual)
            
            # Gera sucessores
            filhos = self.sucessores_grafo(atual.estado, 1)
            
            for novo in filhos:
                if novo not in visitado:
                    # Calcula heurística (distância até o destino)
                    heuristica = self.heuristica_distancia(novo, fim)
                    
                    filho = Node(atual, novo, heuristica, None, None)
                    visitado[novo] = filho
                    
                    # Insere ordenado por heurística
                    self.inserir_ordenado_heuristica(fila, filho)
        
        return None
    
    #--------------------------------------------------------------------------
    # A* (A ESTRELA)
    #--------------------------------------------------------------------------
    def a_estrela(self, inicio, fim):
        """
        Algoritmo A* usando heurística de distância
        """
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em f(n) = g(n) + h(n)
        fila = []
        raiz = Node(None, inicio, 0, None, None)
        fila.append(raiz)
        
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        while fila:
            # Remove o nó com menor f(n)
            atual = fila.pop(0)
            
            # Chegou ao objetivo
            if atual.estado == fim:
                return self.exibirCaminho(atual)
            
            # Gera sucessores
            filhos = self.sucessores_grafo(atual.estado, 1)
            
            for novo in filhos:
                # Custo g(n) = custo do caminho até aqui
                g_novo = atual.v1 + self.grafo_loader.obter_distancia(atual.estado, novo)
                
                # Heurística h(n) = distância até o destino
                h_novo = self.heuristica_distancia(novo, fim)
                
                # f(n) = g(n) + h(n)
                f_novo = g_novo + h_novo
                
                # Se não foi visitado ou encontrou um caminho melhor
                if novo not in visitado or g_novo < visitado[novo].v1:
                    filho = Node(atual, novo, f_novo, None, None)
                    visitado[novo] = filho
                    
                    # Insere ordenado por f(n)
                    self.inserir_ordenado_heuristica(fila, filho)
        
        return None
    
    #--------------------------------------------------------------------------
    # AIA* (A* ITERATIVO)
    #--------------------------------------------------------------------------
    def aia_estrela(self, inicio, fim):
        """
        Algoritmo A* Iterativo usando heurística de distância
        """
        if inicio == fim:
            return [inicio]
        
        # Limite inicial baseado na heurística
        limite = self.heuristica_distancia(inicio, fim)
        
        while True:
            resultado = self.busca_limitada_a_estrela(inicio, fim, limite)
            if resultado is not None:
                return resultado
            
            # Aumenta o limite para a próxima iteração
            limite += 10  # Incremento fixo para simplificar
    
    def busca_limitada_a_estrela(self, inicio, fim, limite):
        """
        Busca A* com limite de custo
        """
        fila = []
        raiz = Node(None, inicio, 0, None, None)
        fila.append(raiz)
        
        visitado = {inicio: raiz}
        
        while fila:
            atual = fila.pop(0)
            
            if atual.estado == fim:
                return self.exibirCaminho(atual)
            
            filhos = self.sucessores_grafo(atual.estado, 1)
            
            for novo in filhos:
                g_novo = atual.v1 + self.grafo_loader.obter_distancia(atual.estado, novo)
                h_novo = self.heuristica_distancia(novo, fim)
                f_novo = g_novo + h_novo
                
                # Só explora se f(n) <= limite
                if f_novo <= limite:
                    if novo not in visitado or g_novo < visitado[novo].v1:
                        filho = Node(atual, novo, f_novo, None, None)
                        visitado[novo] = filho
                        self.inserir_ordenado_heuristica(fila, filho)
        
        return None
    
    def inserir_ordenado_heuristica(self, lista, no):
        """
        Insere nó na lista mantendo ordenação por heurística
        """
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)
