import pygame, time, argparse, csv
import numpy as np
from time import sleep
from numpy.random import randint

class Maze:
    def __init__(self, matriz):
        self.ordem = len(matriz)
        self.matriz = matriz
        self.find_pos_inicio()
        self.find_pos_fim()
        

    def custo_passo(self):
        return 10
    
    def custo_caminho(self, caminho):
        return self.custo_passo() * len(caminho)

    def sucessor(self):

        y = self.pos_atual[0]
        x = self.pos_atual[1]
        resultado = []

        if x >= 0:  # esquerda
            if self.matriz[y][x - 1] == 1:
                resultado.append([y, x - 1])

        if y < self.ordem - 1:  # baixo
            if self.matriz[y + 1][x] == 1:
                resultado.append([y + 1, x])

        if x < self.ordem - 1:  # direita
            if self.matriz[y][x + 1] == 1:
                resultado.append([y, x + 1])

        if y >= 0:  # cima
            if self.matriz[y - 1][x] == 1:
                resultado.append([y - 1, x])

        return resultado

    def teste_objetivo_dfs(self, pos_eval):
        y = pos_eval[0]
        x = pos_eval[1]

        if x < self.ordem - 1:
            if self.matriz[y][x + 1] == 3:
                return 1

        if x >= 0:
            if self.matriz[y][x - 1] == 3:
                return 1

        if y < self.ordem - 1:
            if self.matriz[y + 1][x] == 3:
                return 1

        if y >= 0:
            if self.matriz[y - 1][x] == 3:
                return 1

        return 0

    def dfs(self, pos_eval=None):
        if pos_eval == None:
            pos_eval = self.pos_inicio

        if self.pos_fim in self.caminho:
            return self.caminho

        self.caminho = []
        self.caminho.append(pos_eval)
        self.pos_atual = pos_eval

        if (self.teste_objetivo_dfs(pos_eval)):
            self.caminho.append(self.pos_fim)

            return 1

        for i in self.sucessor():
            if i not in self.caminho:
                next = i
                self.dfs(next)

    def bfs(self):
        self.lista = [self.pos_inicio]
        self.caminho = []

        while self.lista != []:
            aux = self.lista.pop(0)
            self.pos_atual = aux
            self.caminho.append(aux)

            for i in self.sucessor():
                if i not in self.caminho:
                    self.lista.append(i)

        self.caminho.append(self.pos_fim)
        print("Caminho: ", self.caminho)

        return self.caminho
    
    """
    if (self.teste_objetivo(pos_eval)):
            self.percorrido.append(self.pos_fim)
            done = True
            return self.solucao(i), done

        for i in self.sucessor(self.pos_atual,1):
            if i not in self.percorrido:
                next = i
                self.dfs(next)
    """