
class Node(object):
    def __init__(self, pai=None, estado=None, v1=None,anterior=None,  proximo=None):
        self.pai       = pai
        self.estado    = estado
        self.v1        = v1 # Nivel de aprofundamento / Nº de passo para chegar Node
        self.anterior  = anterior
        self.proximo   = proximo

class NodeP(Node):
    def __init__(self, pai=None, estado=None, v1=None,
                 anterior=None, proximo=None, v2=None):
        super().__init__(pai, estado, v1, anterior, proximo)
        self.v2 = v2 # Custo acumulado para chegar a esse Node