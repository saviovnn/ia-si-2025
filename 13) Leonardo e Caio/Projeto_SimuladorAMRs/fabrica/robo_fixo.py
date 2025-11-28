
from enum import Enum
import random


class EstadosFixo(Enum):
    Vazio = 0
    Esperando = 1
    Carregado = 2

class RoboFixo(object):
    
    estado = None
    capMax = None # capacidade maxima
    estoque = None

    posFixo = None # Posição do robo no mapa
    posRecar = None # Posição do local de recarga do mapa

    tick = 0

    def __init__(self, posFixo:tuple, posRecar:tuple, estado:bool, capMax:int):
        self.capMax = capMax
        self.posFixo = posFixo
        self.posRecar = posRecar
        if estado is True:
            self.estado = EstadosFixo.Carregado
            self.estoque = capMax
        else:
            self.estado = EstadosFixo.Vazio
            self.estoque = 0

    def agir(self):

        match(self.estado):
            case EstadosFixo.Vazio:
                return
            case EstadosFixo.Esperando:
                return
            case EstadosFixo.Carregado:
                self.tick += 1

                self.estoque -= random.choice(range(0, 3))

                if self.estoque <= 0:
                    self.tick = 0
                    self.estoque = 0
                    self.estado = EstadosFixo.Vazio


    def solicitar_recarga(self):
        self.estado = EstadosFixo.Esperando
        return self.posRecar, self
    
    def encher_estoque(self):
        self.estado = EstadosFixo.Carregado
        self.estoque = self.capMax