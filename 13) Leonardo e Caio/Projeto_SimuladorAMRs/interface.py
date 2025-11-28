import tkinter as tk
from tkinter import ttk
from collections import deque
import time 
from controller import Controller
from fabrica.robo_fixo import EstadosFixo
from fabrica.amr import AMR, EstadosAMR
from fabrica.central import ControllerCentral

tam_width = 640
tam_height = 360

class Interface():
    def __init__(self, windowMaster):
        self.janela = windowMaster

        self.janela.title("Simulador de AMRs")
        self.janela.resizable(width=False, height=False)
        #self.janela.geometry(f"{tam_width}x{tam_height}")

        self.tileSize = 20
        self.colunas = 32
        self.linhas = 14
        self.width = self.colunas * self.tileSize
        self.height = self.linhas * self.tileSize

        self.coordObs1 = [(7, 8), (7, 9), (7, 10), (7, 11)]
        self.coordObs2 = [(15, 9), (15, 10), (15, 11), (15, 12), (15, 13)]
        self.coordObs3 = [(19, 4), (20, 4), (21, 4), (22, 4), (23, 4)]

        self.coresMapa = {
            0: "white",           #caminho prioridade
            1: "purple",         #caminho pela esteira
            2: "gray",          #caminho possivel
            4: "gray",          #caminho de menor preferencia
            9: "black",          #área segurança
            10: "#e0e000",     #intransitavel
            11: "black",         #AMR
            12: "red",           #maquina fixa  
            13: "#2020FF"      #central

        }

        self.coresRobo = {
            0: "#00DDFF",
            1: "#FF7070",
            2: "#FFFF00",
            3: "#00e000"
        }

        self.estados_rf = {
            0 : "#ffd9d9",
            1 : "#ff9090",
            2 : "#ff0000"
        }

        self.controller = Controller()
        self.central = ControllerCentral(self.controller)
        self.simulacaoRodando = False
        self.velocidade = 100

        self.listRobosFixo = []
        self.listAMR = []
        self.objs = deque()

        # ELEMENTOS INTERFACE
        self.criaWidgets()
        self.desenharMapa()

        # FUNCOES INTERFACE

    def criaWidgets(self):

        # Canvas do mapa
        self.canvas = tk.Canvas(self.janela, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.TOP)


        #frame dos controles
        self.frameControle = tk.Frame(self.janela, bg="#e0e0e0", height=self.tileSize*4)
        self.frameControle.pack(side=tk.BOTTOM, fill=tk.X)


        #botão ligar/desligar
        self.buttonIniciar = tk.Button(self.frameControle, text="Inicial/reiniciar", command=self.iniciarSimulacao)
        self.buttonIniciar.pack(side=tk.LEFT, padx=10, pady=5)

        self.buttonParar = tk.Button(self.frameControle, text="Desligar", command=self.pararSimulacao, state=tk.DISABLED)
        self.buttonParar.pack(side=tk.LEFT, padx=10, pady=5)


        #controle velocidade
        labelVel = tk.Label(self.frameControle, text="Velocidade:", bg="#e0e0e0")
        labelVel.pack(side=tk.LEFT, padx=(20, 5))

        self.boxVel = ttk.Combobox(self.frameControle, values=["Lento", "Normal", "Rápido"], state="readonly", width=10)
        self.boxVel.current(1)
        self.boxVel.bind("<<ComboboxSelected>>", self.alterarVel)
        self.boxVel.pack(side=tk.LEFT, padx=5)


        #Obstaculos (implementar depois)
        self.checkObstaculo1 = tk.IntVar()
        self.checkObstaculo2 = tk.IntVar()
        self.checkObstaculo3 = tk.IntVar()

        tk.Checkbutton(self.frameControle, text="Obs. A", variable=self.checkObstaculo1, command=self.criarObstaculos, bg="#e0e0e0").pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(self.frameControle, text="Obs. B", variable=self.checkObstaculo2, command=self.criarObstaculos, bg="#e0e0e0").pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(self.frameControle, text="Obs. C", variable=self.checkObstaculo3, command=self.criarObstaculos, bg="#e0e0e0").pack(side=tk.LEFT, padx=5)



    def criarObstaculos(self):
        mapaBase = self.controller.mapaBase
        mapaTemp = self.controller.mapaTemp

        for x in range(self.colunas):
            for y in range(self.linhas):
                if x < len(mapaBase) and y < len(mapaBase[0]):
                    mapaTemp[x][y] = mapaBase[x][y]


        if self.checkObstaculo1.get() == 1:
            for coord in self.coordObs1:
                if coord[0] < self.colunas and coord[1] < self.linhas:
                    mapaTemp[coord[0]][coord[1]] = 9

        if self.checkObstaculo2.get() == 1:
            for coord in self.coordObs2:
                if coord[0] < self.colunas and coord[1] < self.linhas:
                    mapaTemp[coord[0]][coord[1]] = 9

        if self.checkObstaculo3.get() == 1:
            for coord in self.coordObs3:
                if coord[0] < self.colunas and coord[1] < self.linhas:
                    mapaTemp[coord[0]][coord[1]] = 9


        self.desenharMapa()


    def alterarVel(self, event):
        choice = self.boxVel.get()

        if choice == "Lento": 
            self.velocidade = 300
        elif choice == "Normal":
            self.velocidade = 100
        elif choice == "Rápido":
            self.velocidade = 50


    def iniciarSimulacao(self):
        if not self.simulacaoRodando:
            self.central.reset_simulacao()
            self.criarObstaculos()

            self.simulacaoRodando = True
            self.buttonParar.config(state=tk.NORMAL)
            self.desenharMapa()
            self.loopSimulacao()
        else:
            self.simulacaoRodando = False
            self.janela.after(self.velocidade + 50, self.iniciarSimulacao)

    def pararSimulacao(self):
        self.central.reset_simulacao()
        self.simulacaoRodando = False
        self.buttonParar.config(state=tk.DISABLED)
        self.desenharMapa()

    def loopSimulacao(self):
        if not self.simulacaoRodando:
            return
        
        self.central.agir()      

        self.desenharMapa()
        self.janela.after(self.velocidade, self.loopSimulacao)


    def desenharMapa(self):
        self.canvas.delete("all")
        mapa = self.controller.mapaTemp

        for y in range(self.linhas):
            for x in range(self.colunas):
                if x < len(mapa) and y < len(mapa[0]):
                    valor = mapa[x][y]
                    cor = self.coresMapa.get(valor, "White")

                    self.canvas.create_rectangle(
                        x * self.tileSize, y * self.tileSize,
                        (x + 1) * self.tileSize, (y + 1) * self.tileSize,
                        fill=cor, outline="lightgray"
                    )

        for fixo in self.central.listRobosFixo:
            ts = self.tileSize
            # Representação do Robo fixo
            fx, fy = fixo.posFixo
            cor = self.estados_rf.get(fixo.estado.value)
            
            self.canvas.create_rectangle(
                fx * ts, fy * ts,
                (fx + 1) * ts, (fy + 1) * ts,
                fill=cor, outline="lightgray"
            )
            # Representação do local de recarga do robo
            cx, cy = fixo.posRecar
            self.canvas.create_rectangle(
                (cx * ts)+6, (cy * ts)+6,
                ((cx + 1) * ts)-6, ((cy + 1) * ts)-6,
                fill="green", outline="lightgray"
            )

        for i, robo in enumerate(self.central.listAMR):
            rx, ry = robo.posAtual
            cor = self.coresRobo.get(i, "White")
            self.canvas.create_oval(
                rx * self.tileSize + 2, ry * self.tileSize + 2,
                (rx + 1) * self.tileSize - 2, (ry + 1) * self.tileSize - 2,
                fill=cor, outline="black", width=2
            )

        