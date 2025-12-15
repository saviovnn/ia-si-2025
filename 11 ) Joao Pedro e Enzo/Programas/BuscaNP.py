from collections import deque
from Node import Node
from NodeP import NodeP
import heapq

class buscaNP(object):
    def __init__(self):
        self.heuristicaS = {}
    
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRAFO
    #--------------------------------------------------------------------------
    def sucessores_grafo(self, ind, grafo, ordem):
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
    
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRAFO 2
    #--------------------------------------------------------------------------
    def sucessores_grafo2(self, ind, grafo, ordem):
        f = []
        for j, (viz, peso) in enumerate(grafo[ind][::ordem]):
            if peso != 0:  # já é inteiro
                f.append((str(viz), int(peso)))  # tupla (estado, peso)
        return f
    
    #--------------------------------------------------------------------------
    # CONTROLE DE NÓS REPETIDOS
    #--------------------------------------------------------------------------
    def verificaVisitado(self, novo, nivel, visitado):
        flag = True  # controle de nós repetidos
        for aux in visitado:
            if aux[0] == novo:
                if aux[1] <= (nivel + 1):
                    flag = False
                else:
                    aux[1] = nivel + 1
                break
        return flag
    
    #--------------------------------------------------------------------------
    # EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
    #--------------------------------------------------------------------------
    def exibirCaminho(self, node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
    
    #--------------------------------------------------------------------------
    # CONTROLE DE NÓS REPETIDOS
    #--------------------------------------------------------------------------
    def exibirCaminho1(self, encontro, visitado1, visitado2):
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
    # INSERE NA LISTA MANTENDO-A ORDENADA
    #--------------------------------------------------------------------------
    def inserir_ordenado(self, lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)
    
    #--------------------------------------------------------------------------
    # Metodo Auxiliar Heuristisca
    #--------------------------------------------------------------------------
    def heuristica(self, nos, grafo, destino):
        if destino in getattr(self, 'heuristicaS', {}):
            return self.heuristicaS[destino]
        
        dist = {n: float("inf") for n in nos}
        dist[destino] = 0
        fila = [(0, destino)]
        heapq.heapify(fila)
        
        while fila:
            custo_atual, atual = heapq.heappop(fila)
            if custo_atual > dist[atual]:
                continue
            
            # Recupera vizinhos do nó atual
            idx = nos.index(atual)
            vizinhos = grafo[idx]  # espera lista de [viz, peso]
            
            for vizinho, peso in vizinhos:
                vizinho = str(vizinho)
                peso = int(peso)
                novo_custo = custo_atual + peso
                if novo_custo < dist[vizinho]:
                    dist[vizinho] = novo_custo
                    heapq.heappush(fila, (novo_custo, vizinho))
        
        self.heuristicaS[destino] = dist
        return dist
    
    #--------------------------------------------------------------------------
    # GERA H
    #--------------------------------------------------------------------------
    def heuristica_grafo(self, nos, n, destino, grafo):
        heuristicas = self.heuristica(nos, grafo, destino)
        return heuristicas.get(n, float("inf"))
    
    # -----------------------------------------------------------------------------
    # A ESTRELA
    # -----------------------------------------------------------------------------
    def a_estrela(self, inicio, fim, nos, grafo, MostrarRotas=True):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        raiz = NodeP(None, inicio, 0, None, None, 0)
        lista.append(raiz)
        
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
            
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho_ida = self.exibirCaminho(atual)
                custo_ida = atual.v2
                
                if MostrarRotas == True:
                    caminho_volta, custo_volta = self.a_estrela(fim, inicio, nos, grafo, MostrarRotas=False)
                    caminho_total = caminho_ida + caminho_volta[1:]
                    custo_total = custo_ida + custo_volta
                    
                    print("\nIda:", caminho_ida, " | Custo:", custo_ida)
                    print("Volta:", caminho_volta, " | Custo:", custo_volta)
                    print("Rota Completa:", caminho_total, " | Custo total:", custo_total, "\n")
                    return caminho_total, custo_total
                
                return caminho_ida, custo_ida
            
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo2(ind, grafo, 1)
            
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                h = self.heuristica_grafo(nos, novo[0], fim, grafo)
                v1 = v2 + h
                
                # relaxamento: nunca visto ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2)
                    visitado[novo[0]] = filho
                    self.inserir_ordenado(lista, filho)
        
        # Sem caminho
        return None, float("inf")