
class Maze:
    def __init__(self, matriz):
        self.ordem = len(matriz)
        self.matriz = matriz
        self.find_pos_inicio()
        self.find_pos_fim()
        self.pos_atual = self.pos_inicio
        self.caminho = []

        print("\nINICIO DFS: \n")
        self.dfs(self.pos_inicio)
        print("\n")

    def find_pos_inicio(self):
        for i in range(self.ordem):  # linha
            for j in range(self.ordem):  # coluna
                if self.matriz[i][j] == 2:
                    self.pos_inicio = [i, j]  # linha,coluna
        print("Pos inicio: ", self.pos_inicio)

    def find_pos_fim(self):
        for i in range(self.ordem):
            for j in range(self.ordem):
                if self.matriz[i][j] == 3:
                    self.pos_fim = [i, j]
        print("Pos fim: ", self.pos_fim)

    def sucessor(self):

        y = self.pos_atual[0]
        x = self.pos_atual[1]
        resultado = []

        if x >= 0:  #esquerda
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

    def teste_objetivo(self, pos_eval):
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

    def dfs(self, pos_eval):
        if self.pos_fim in self.caminho:
            return 1
        
        print(pos_eval)
        self.caminho.append(pos_eval)
        self.pos_atual = pos_eval

        if (self.teste_objetivo(pos_eval)):
            print("FIM", self.pos_fim)
            self.caminho.append(self.pos_fim)
            return 1
        
        for i in self.sucessor():
            if i not in self.caminho:
                next = i
                
                self.dfs(next)
      
if __name__ == "__main__":
    # aaaaaaaa#0 #1 #2 #3 #4 #5 #6 #7 #8 #9
    matriz = [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
              [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 3
              [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],  # 4
              [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],  # 5
              [0, 0, 1, 1, 1, 1, 0, 1, 0, 0],  # 6
              [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],  # 7
              [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],  # 8
              [0, 0, 1, 3, 1, 1, 1, 1, 0, 0]]  # 9
    for i in matriz:
        print(i)

    maze = Maze(matriz)
