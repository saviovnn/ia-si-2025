
from collections import deque
from fabrica.amr import AMR, EstadosAMR
from fabrica.robo_fixo import EstadosFixo, RoboFixo


class ControllerCentral():
    
    control = None
    listRobosFixo = None
    listAMR = None
    listChamadas = None

    def __init__(self, controller):
        self.control = controller
        self.init_simulacao()

    
    def init_simulacao(self):
        self.listRobosFixo = [
            self.control.create_robo_fixo((4, 2), (4, 1), False, 150),
            self.control.create_robo_fixo((4, 3), (4, 4), True, 150),
            self.control.create_robo_fixo((8, 3), (9, 3), True, 200),
            self.control.create_robo_fixo((10, 2), (11, 2), False, 200),
            self.control.create_robo_fixo((9, 7), (8, 7), True, 250),
            self.control.create_robo_fixo((19, 3), (19, 2), False, 200),
            self.control.create_robo_fixo((19, 6), (19, 5), False, 200),
            self.control.create_robo_fixo((23, 3), (23, 2), True, 200),
            self.control.create_robo_fixo((23, 6), (23, 5), True, 250),
            self.control.create_robo_fixo((27, 2), (26, 2), True, 150),
            self.control.create_robo_fixo((28, 6), (28, 5), True, 300),
            self.control.create_robo_fixo((28, 10), (28, 9), True, 350),
        ]
        self.listAMR = [
            AMR( (4,  9), True, self.control),
            AMR( (4, 10), True, self.control),
            AMR( (4, 11), True, self.control),
            AMR( (4, 12), True, self.control),
        ]
        self.listChamadas = deque()


    def agir(self):
        ## Colocar essa parte dentro do método de loop do interface
        for fixo in self.listRobosFixo :
            fixo.agir()
            if fixo.estado == EstadosFixo.Vazio:
                self.listChamadas.append(fixo.solicitar_recarga())

        for i, robo in enumerate(self.listAMR):
            #print("------- AMR ", i)
            #print("Estado: ", robo.estado.name)
            robo.agir()

            if robo.estado == EstadosAMR.Alerta:
                if len(self.listChamadas) != 0:
                    obj = self.listChamadas.popleft()
                    robo.set_objetivo(obj[0], obj[1])


    def reset_simulacao(self):
        self.control.mapaTemp = self.control.CriarMapaArquivo("models/txts/mapaSala.txt")
        self.init_simulacao()