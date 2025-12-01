from fabrica.robo_fixo import RoboFixo
from models.buscaGrid import BuscaGrid

pathMapaSala = "models/txts\mapaSala.txt"

class Controller():

    mapaBase = None
    mapaTemp = None
    busca = None

    largura = None
    altura = None

    def __init__(self):
        self.busca = BuscaGrid()
        self.mapaBase = self.CriarMapaArquivo(pathMapaSala)
        self.mapaTemp = self.CriarMapaArquivo(pathMapaSala)

    def CriarMapaArquivo(self, arquivo):
        # Lê todas as linhas e já divide em colunas
        with open(arquivo, "r") as txt:
            linhas = [linha.strip().split(",") for linha in txt]

        # Descobre tamanho
        self.altura  = len(linhas)  # Y = número de linhas
        self.largura = len(linhas[0])     # X = número de colunas

        # Cria a matriz [X][Y] diretamente
        matriz = [[int(linhas[y][x]) for y in range(self.altura)] for x in range(self.largura)]
        return matriz
    

    def DesenharGrid(self, mapa): # Print
        lenX = len(mapa)
        lenY = len(mapa[0])

        print("Desenho da Matriz: ")

        linha = "     "
        for i in range(lenX):
            linha += f"{i:>2}  "
        print(linha)

        print("   + " + ("----"*(lenX-1)) + "-")

        for y in range(lenY):          # percorre linhas
            txt = f"{y:0>2} | "

            for x in range(lenX):         # percorre colunas
                txt += f"{mapa[x][y]:>2}  "
            print(txt)
        print("   + " + ("---"*(lenX-1)) + "-")
    

    def create_robo_fixo(self, posFixo, posRecar, estado, capMax):
        self.mapaTemp[posFixo[0]][posFixo[1]] = 12
        return RoboFixo(posFixo, posRecar, estado, capMax)


    def pros_passo_ia(self, posAtual, posAlvo):
        caminho = self.busca.a_estrela(posAtual, posAlvo, self.largura, self.altura, self.mapaTemp)
        if caminho == None:
            return None
        passo = caminho[1]

        self.mapaTemp[posAtual[0]][posAtual[1]] = self.mapaBase[posAtual[0]][posAtual[1]]
        self.mapaTemp[passo[0]][passo[1]] = 11

        return passo