from enum import Enum
import random
from models.buscaGrid import BuscaGrid

class EstadosAMR(Enum):
    Desligado = -1
    Ocioso = 0
    Alerta = 1
    CaminhoAlvo = 2
    CaminhoBase = 3
    Reabastecendo = 4
    Esperando = 5


class AMR(object):

    estado   = None
    control  = None

    posAtual = None

    posAlvo  = None
    posBase  = None
    roboAlvo = None

    tempEspera = random.randrange(1, 6)
    tick = 0

    def __init__(self, posBase:tuple, ligado:bool, controller):
        self.posBase = posBase
        self.posAtual = posBase
        self.estado = EstadosAMR.Ocioso if ligado is True else EstadosAMR.Desligado
        self.control = controller
        self.control.mapaTemp[self.posAtual[0]][self.posAtual[1]] = 11


    def agir(self):

        match(self.estado):
            case EstadosAMR.Desligado:
                return
            
            case EstadosAMR.Ocioso:
                if self.tick == 5:
                    self.tick = 0
                    self.estado = EstadosAMR.Alerta
                self.tick += 1
                
            case EstadosAMR.Alerta:
                if self.tick == 3:
                    self.tick = 0
                    self.estado = EstadosAMR.Ocioso
                self.tick += 1
                
            case EstadosAMR.CaminhoAlvo:
                if self.posAtual != self.posAlvo:
                    prosPasso = self.control.pros_passo_ia(self.posAtual, self.posAlvo)
                    if prosPasso != None:
                        self.posAtual = prosPasso
                    else:
                        self.tick = 0
                        self.estado = EstadosAMR.Esperando
                else:
                    self.tick = 0
                    self.posAlvo = None
                    self.estado = EstadosAMR.Reabastecendo

            case EstadosAMR.CaminhoBase:
                if self.posAtual != self.posBase:
                    prosPasso = self.control.pros_passo_ia(self.posAtual, self.posBase)
                    if prosPasso != None:
                        self.posAtual = prosPasso
                    else:
                        self.tick = 0
                        self.estado = EstadosAMR.Esperando
                else:
                    self.tick = 0
                    self.estado = EstadosAMR.Ocioso

            case EstadosAMR.Reabastecendo:
                if self.tick == 5:
                    self.tick = 0
                    self.roboAlvo.encher_estoque()
                    self.estado = EstadosAMR.CaminhoBase
                self.tick += 1
            
            case EstadosAMR.Esperando:
                if self.tick == self.tempEspera:
                    self.tick = 0
                    if self.posAlvo != None:
                        self.estado = EstadosAMR.CaminhoAlvo
                    else:
                        self.estado = EstadosAMR.CaminhoBase
                self.tick += 1



    def set_objetivo(self, pos, roboAlvo):
        self.tick = 0
        self.posAlvo = pos
        self.roboAlvo = roboAlvo
        self.estado = EstadosAMR.CaminhoAlvo