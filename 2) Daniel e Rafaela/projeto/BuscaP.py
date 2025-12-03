from collections import deque
from NodeP import NodeP

class busca(object):
    #-----------------------------------------------------------------------------
    # GERA O GRID DE ARQUIVO TEXTO
    #-----------------------------------------------------------------------------
    def Gera_Problema_Grid_Fixo(self, arquivo):
        file = open(arquivo)
        mapa = []
        for line in file:
            aux_str = line.strip("\n")
            aux_str = aux_str.split(",")
            aux_int = [int(x) for x in aux_str]
            mapa.append(aux_int)
        nx = len(mapa)
        ny = len(mapa[0])
        return mapa,nx,ny
    
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
    # SUCESSORES PARA GRID
    #--------------------------------------------------------------------------
    def sucessores_grid_ponderado(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        
        if mapa[x][y] == 9:
            return f
        
        # DIREITA
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)        
        return f

    #--------------------------------------------------------------------------
    # DISTÂNCIA MANHATTAN
    #--------------------------------------------------------------------------

    def manhattan(self, atual, fim):
        x1, y1 = atual
        x2, y2 = fim
        return abs(x1 - x2) + abs(y1 - y2)

    #--------------------------------------------------------------------------    
    # INSERE NA LISTA MANTENDO-A ORDENADA
    #--------------------------------------------------------------------------    
    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)

    # -----------------------------------------------------------------------------
    # A ESTRELA
    # -----------------------------------------------------------------------------
    def a_estrela(self,inicio,fim,mapa,nx,ny):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        t_inicio = tuple(inicio)
        
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
                caminho = self.exibirCaminho(atual)
                return caminho
            filhos = self.sucessores_grid_ponderado(atual.estado, nx, ny, mapa)
    
            for novo in filhos:
                pos = tuple(novo[0])
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 + self.manhattan(pos,fim) 
    
                # relaxamento: nunca visto ou custo melhor
                if (pos not in visitado) or (v2 < visitado[pos].v2):
                    filho = NodeP(atual, pos, v1, None, None, v2)
                    visitado[pos] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None