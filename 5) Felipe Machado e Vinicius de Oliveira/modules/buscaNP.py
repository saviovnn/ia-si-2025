from collections import deque
from modules.Node import Node
from modules.NodeP import NodeP
from math import sqrt

class buscaNP(object):
    #--------------------------------------------------------------------------  
    # SUCESSORES PARA GRID (LISTA DE ADJACÊNCIAS)  
    #--------------------------------------------------------------------------  
    def sucessores_grid(self, st, nx, ny, mapa):
        f = []
        x, y = st[0], st[1]
        validos = (0, 2)

        if y+1 < ny and mapa[x][y+1] in validos:
            f.append([x, y+1])
        if y-1 >= 0 and mapa[x][y-1] in validos:
            f.append([x, y-1])
        if x+1 < nx and mapa[x+1][y] in validos:
            f.append([x+1, y])
        if x-1 >= 0 and mapa[x-1][y] in validos:
            f.append([x-1, y])

        return f


    def sucessores_grid_custo(self, st, nx, ny, mapa):
        f = []
        custo = 5
        x, y = st[0], st[1]
        validos = (0, 2)

        if y+1 < ny and mapa[x][y+1] in validos:
            f.append(([x, y+1], custo))
        if y-1 >= 0 and mapa[x][y-1] in validos:
            f.append(([x, y-1], custo))
        if x+1 < nx and mapa[x+1][y] in validos:
            f.append(([x+1, y], custo))
        if x-1 >= 0 and mapa[x-1][y] in validos:
            f.append(([x-1, y], custo))

        return f

    #--------------------------------------------------------------------------    
    # EXIBE O CAMINHO ENCONTRADO  
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
        encontro1 = visitado1[encontro]  
        encontro2 = visitado2[encontro]
        caminho1 = self.exibirCaminho(encontro1)
        caminho2 = self.exibirCaminho(encontro2)
        caminho2 = list(reversed(caminho2[:-1]))
        return caminho1 + caminho2

    #--------------------------------------------------------------------------  
    # BUSCA EM AMPLITUDE (BFS)  
    #--------------------------------------------------------------------------  
    def amplitude(self,inicio,fim,nx,ny,mapa):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        fila = deque()
        raiz = Node(None,t_inicio,0,None,None)
        fila.append(raiz)
        visitado = {t_inicio: raiz}
        while fila:
            atual = fila.popleft()
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
            for novo in filhos:
                t_novo = tuple(novo)
                if t_novo not in visitado:
                    filho = Node(atual,t_novo,atual.v1 + 1,None,None)
                    fila.append(filho)
                    visitado[t_novo] = filho
                    if t_novo == t_fim:
                        return self.exibirCaminho(filho)
        return None

    #--------------------------------------------------------------------------  
    # BUSCA EM PROFUNDIDADE (DFS)  
    #--------------------------------------------------------------------------  
    def profundidade(self,inicio,fim,nx,ny,mapa):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        pilha = deque()
        raiz = Node(None,t_inicio,0,None,None)
        pilha.append(raiz)
        visitado = {t_inicio: raiz}
        while pilha:
            atual = pilha.pop()
            filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
            for novo in filhos:
                t_novo = tuple(novo)
                if t_novo not in visitado:
                    filho = Node(atual,t_novo,atual.v1 + 1,None,None)
                    pilha.append(filho)
                    visitado[t_novo] = filho
                    if t_novo == t_fim:
                        return self.exibirCaminho(filho)
        return None

    #--------------------------------------------------------------------------  
    # BUSCA EM PROFUNDIDADE LIMITADA  
    #--------------------------------------------------------------------------  
    def prof_limitada(self,inicio,fim,nx,ny,mapa,lim):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        pilha = deque()
        raiz = Node(None,t_inicio,0,None,None)
        pilha.append(raiz)
        visitado = {t_inicio: raiz}
        while pilha:
            atual = pilha.pop()
            if atual.v1 < lim:
                filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
                for novo in filhos:
                    t_novo = tuple(novo)
                    if t_novo not in visitado:
                        filho = Node(atual,t_novo,atual.v1 + 1,None,None)
                        pilha.append(filho)
                        visitado[t_novo] = filho
                        if t_novo == t_fim:
                            return self.exibirCaminho(filho)
        return None

    #--------------------------------------------------------------------------  
    # BUSCA EM APROFUNDAMENTO ITERATIVO  
    #--------------------------------------------------------------------------  
    def aprof_iterativo(self,inicio,fim,nx,ny,mapa,lim_max):
        for lim in range(1,lim_max):
            if inicio == fim:
                return [inicio]
            t_inicio = tuple(inicio)
            t_fim = tuple(fim)
            pilha = deque()
            raiz = Node(None,t_inicio,0,None,None)
            pilha.append(raiz)
            visitado = {t_inicio: raiz}
            while pilha:
                atual = pilha.pop()
                if atual.v1 < lim:
                    filhos = self.sucessores_grid(atual.estado,nx,ny,mapa)
                    for novo in filhos:
                        t_novo = tuple(novo)
                        if t_novo not in visitado:
                            filho = Node(atual,t_novo,atual.v1 + 1,None,None)
                            pilha.append(filho)
                            visitado[t_novo] = filho
                            if t_novo == t_fim:
                                return self.exibirCaminho(filho)
        return None

    #--------------------------------------------------------------------------  
    # BUSCA BIDIRECIONAL  
    #--------------------------------------------------------------------------  
    def bidirecional(self, inicio, fim, nx, ny, mapa):
        if inicio == fim:
            return [inicio]
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        fila1 = deque()
        fila2 = deque()
        raiz1 = Node(None, t_inicio, 0, None, None)
        raiz2 = Node(None, t_fim, 0, None, None)
        fila1.append(raiz1)
        fila2.append(raiz2)
        visitado1 = {t_inicio: raiz1}
        visitado2 = {t_fim: raiz2}
        while fila1 and fila2:
            for _ in range(len(fila1)):
                atual = fila1.popleft()
                filhos = self.sucessores_grid(atual.estado, nx, ny, mapa)
                for novo in filhos:
                    t_novo = tuple(novo)
                    if t_novo not in visitado1:
                        filho = Node(atual, t_novo, atual.v1 + 1, None, None)
                        visitado1[t_novo] = filho
                        fila1.append(filho)
                        if t_novo in visitado2:
                            return self.exibirCaminho1(t_novo, visitado1, visitado2)
            for _ in range(len(fila2)):
                atual = fila2.popleft()
                filhos = self.sucessores_grid(atual.estado, nx, ny, mapa)
                for novo in filhos:
                    t_novo = tuple(novo)
                    if t_novo not in visitado2:
                        filho = Node(atual, t_novo, atual.v1 + 1, None, None)
                        visitado2[t_novo] = filho
                        fila2.append(filho)
                        if t_novo in visitado1:
                            return self.exibirCaminho1(t_novo, visitado1, visitado2)
        return None

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

    #--------------------------------------------------------------------------    
    # GERA H - GRID
    #--------------------------------------------------------------------------    
    def heuristica_grid(self,p1,p2):
        if (p2[0]-p1[0])<0:
            c1 = 3
        else:
            c1 = 2
        if (p2[1]-p1[1])<0:
            c2 = 7
        else:
            c2 = 5
        h = sqrt(c1*(p1[0]-p2[0])**2 + c2*(p1[1]-p2[1])**2)
        return h

    # -----------------------------------------------------------------------------    
    # CUSTO UNIFORME 
    # -----------------------------------------------------------------------------    
    def custo_uniforme(self, inicio, fim, mapa, nx, ny):
        if inicio == fim:
            return [inicio], 0
        
        lista = []
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        raiz = NodeP(None, t_inicio, 0, None, None, 0)  
        lista.append(raiz)
        visitado = {t_inicio: raiz}
        
        while lista:
            atual_idx = 0
            for i in range(1, len(lista)):
                if lista[i].v1 < lista[atual_idx].v1:
                    atual_idx = i
            atual = lista.pop(atual_idx)
            
            if atual.estado == t_fim:
                return self.exibirCaminho(atual), atual.v1

            filhos = self.sucessores_grid_custo(atual.estado, nx, ny, mapa)
            for pos, custo in filhos:
                t_novo = tuple(pos)
                novo_custo = atual.v1 + custo           
                if t_novo not in visitado or novo_custo < visitado[t_novo].v1:
                    filho = NodeP(atual, t_novo, novo_custo, None, None, novo_custo)
                    if t_novo in visitado:
                        for i, node in enumerate(lista):
                            if node.estado == t_novo:
                                lista.pop(i)
                                break
                    
                    lista.append(filho)
                    visitado[t_novo] = filho
                    
        return None

    # -----------------------------------------------------------------------------    
    # GREEDY 
    # -----------------------------------------------------------------------------    
    def greedy(self, inicio, fim, mapa, nx, ny):
        if inicio == fim:
            return [inicio], 0
        
        lista = []
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        h_inicio = self.heuristica_grid(inicio, fim)
        raiz = NodeP(None, t_inicio, h_inicio, None, None, 0)  
        lista.append(raiz)
        visitado = {t_inicio: raiz}
        
        while lista:
            atual_idx = 0
            for i in range(1, len(lista)):
                if lista[i].v1 < lista[atual_idx].v1:
                    atual_idx = i
            atual = lista.pop(atual_idx)
            
            if atual.estado == t_fim:
                return self.exibirCaminho(atual), atual.v2

            filhos = self.sucessores_grid_custo(atual.estado, nx, ny, mapa)
            for pos, custo in filhos:
                t_novo = tuple(pos)
                novo_custo = atual.v2 + custo
                h_novo = self.heuristica_grid(pos, fim)
                
                if t_novo not in visitado:
                    filho = NodeP(atual, t_novo, h_novo, None, None, novo_custo)
                    lista.append(filho)
                    visitado[t_novo] = filho
                    
        return None

    # -----------------------------------------------------------------------------    
    # A ESTRELA 
    # -----------------------------------------------------------------------------    
    def a_estrela(self, inicio, fim, mapa, nx, ny):
        if inicio == fim:
            return [inicio], 0
        
        lista = []
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        h_inicio = self.heuristica_grid(inicio, fim)
        raiz = NodeP(None, t_inicio, h_inicio, None, None, 0)  
        lista.append(raiz)
        visitado = {t_inicio: raiz}
        
        while lista:
            atual_idx = 0
            for i in range(1, len(lista)):
                if lista[i].v1 < lista[atual_idx].v1:
                    atual_idx = i
            atual = lista.pop(atual_idx)
            
            if atual.estado == t_fim:
                return self.exibirCaminho(atual), atual.v2

            filhos = self.sucessores_grid_custo(atual.estado, nx, ny, mapa)
            for pos, custo in filhos:
                t_novo = tuple(pos)
                g_novo = atual.v2 + custo  
                h_novo = self.heuristica_grid(pos, fim)
                f_novo = g_novo + h_novo   
                if t_novo not in visitado or f_novo < visitado[t_novo].v1:
                    filho = NodeP(atual, t_novo, f_novo, None, None, g_novo)
                    if t_novo in visitado:
                        for i, node in enumerate(lista):
                            if node.estado == t_novo:
                                lista.pop(i)
                                break
                    
                    lista.append(filho)
                    visitado[t_novo] = filho
                    
        return None

    # -----------------------------------------------------------------------------    
    # AI ESTRELA 
    # -----------------------------------------------------------------------------       
    def aia_estrela(self, inicio, fim, mapa, nx, ny):
        if inicio == fim:
            return [inicio], 0
        
        limite = self.heuristica_grid(inicio, fim)
        max_iterations = 100  
        
        for _ in range(max_iterations):
            resultado = self.busca_limite_aia(inicio, fim, mapa, nx, ny, limite)
            if resultado is not None:
                return resultado
            limite *= 1.5
            
        return None

    def busca_limite_aia(self, inicio, fim, mapa, nx, ny, limite):
        lista = []
        t_inicio = tuple(inicio)
        t_fim = tuple(fim)
        h_inicio = self.heuristica_grid(inicio, fim)
        raiz = NodeP(None, t_inicio, h_inicio, None, None, 0)
        lista.append(raiz)
        visitado = {t_inicio: raiz}
        menor_excedente = float('inf')
        
        while lista:
            atual_idx = 0
            for i in range(1, len(lista)):
                if lista[i].v1 < lista[atual_idx].v1:
                    atual_idx = i
            atual = lista.pop(atual_idx)
            
            if atual.estado == t_fim:
                return self.exibirCaminho(atual), atual.v2

            filhos = self.sucessores_grid_custo(atual.estado, nx, ny, mapa)
            for pos, custo in filhos:
                t_novo = tuple(pos)
                g_novo = atual.v2 + custo
                h_novo = self.heuristica_grid(pos, fim)
                f_novo = g_novo + h_novo
                
                if f_novo <= limite:
                    if t_novo not in visitado or f_novo < visitado[t_novo].v1:
                        filho = NodeP(atual, t_novo, f_novo, None, None, g_novo)
                        
                        if t_novo in visitado:
                            for i, node in enumerate(lista):
                                if node.estado == t_novo:
                                    lista.pop(i)
                                    break
                        
                        lista.append(filho)
                        visitado[t_novo] = filho
                else:
                    if f_novo < menor_excedente:
                        menor_excedente = f_novo
        
        if menor_excedente != float('inf'):
            return None
        else:
            return None