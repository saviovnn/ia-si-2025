import math
from collections import deque
from models.node import NodeP

class BuscaGrid():

    # ===== Métodos auxiliades ===========================================
    def sucessores(self, pos, largura, altura, mapa, ponderado):
        sucs = [] # Sucessores, proximos caminhos possiveis
        x, y, = pos[0], pos[1]

        # Ponderado = [pos, custo, pos, custo, ...]

        # Direita -----
        if(y+1<altura):
            if(mapa[x][y+1]<9):
                sucs.append((x,y+1))
                # Busca ponderada
                if(ponderado): 
                    sucs.append(int(mapa[x][y+1])) # peso do tile
        # Esquerda -----
        if(y-1>=0):
            if(mapa[x][y-1]<9):
                sucs.append((x,y-1))
                # Busca ponderada
                if(ponderado): 
                    sucs.append(int(mapa[x][y-1])) # peso do tile
        # Abaixo -----
        if(x+1<largura):
            if(mapa[x+1][y]<9):
                sucs.append((x+1,y))
                # Busca ponderada
                if(ponderado): 
                    sucs.append(int(mapa[x+1][y])) # peso do tile
        # Acima -----
        if(x-1>=0):
            if(mapa[x-1][y]<9):
                sucs.append((x-1,y))
                # Busca ponderada
                if(ponderado): 
                    sucs.append(int(mapa[x-1][y])) # peso do tile

        return sucs


    def exibir_caminho(self, node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho


    def inserir_ordenado(self,lista, no): # para Fila de prioridade
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)
    
    
    def heuristica(self, atual, fim): # Para grade, usando a Distância de Manhattan
        h = math.fabs(fim[0]-atual[0]) + math.fabs(fim[1]-atual[1])
        return h


    # ===== Métodos de busca =============================================
    def a_estrela(self, inicio, fim, largura, altura, mapa):
        # Retorna se o inicio por o mesmo que o fim
        if inicio == fim: 
            return [inicio]

        # Criado estruturas de dados
        filaP = deque()
        visitado = {}

        # Iniciando a busca com a raiz
        raiz = NodeP(None, inicio, 0, None, None, 0)
        filaP.append(raiz)
        visitado[inicio] = raiz
    
        # Iniciando a procura em outros Nodes
        while filaP:
            atual = filaP.popleft()
            valor_atual = atual.v2

            if(atual.estado == fim): # Achou um caminho
                caminho = self.exibir_caminho(atual)
                return caminho

            # Avançando para a proxiam tuple na lista | [pos, custo, pos, custo, ...]
            filhos = self.sucessores(atual.estado, largura, altura, mapa, True)

            i = 0
            while i < len(filhos):
                novo = filhos[i]
                v2 = valor_atual + filhos[i+1]
                v1 = v2 + self.heuristica(filhos[i], fim)
                
                if(novo not in visitado) or (v2 < visitado[novo].v2):
                    filho = NodeP(atual, novo, v1, 0, None, v2)
                    visitado[novo] = filho
                    self.inserir_ordenado(filaP, filho)

                i += 2
        # Não achou um caminho
        #print("Caminho não encontrado.")
        return None