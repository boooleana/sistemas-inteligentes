import pygame, time, argparse, csv
import numpy as np
from time import sleep
from numpy.random import randint

class Node:
    def __init__(self, pos, parent):
        self.x = pos[0]
        self.y = pos[1]
        self.parent = parent

    def position(self):
        return (self.x, self.y)

class Maze:
    def __init__(self, pos_inicio, pos_fim, matriz,ordem):
        self.ordem = ordem
        self.matriz = matriz
        self.pos_inicio = pos_inicio
        self.pos_fim = pos_fim
    
    def sucessor(self,node,valor):
        (x,y) = node.position()
        (max_x,max_y) = self.ordem 
        resultado = []

        for mov in [(1,0), (-1,0), (0,1), (0,-1)]:
            new_pos = (x+mov[0],y+mov[1])
            x_in = (new_pos[0] <= max_x) & (new_pos[0] >= 0) 
            y_in = (new_pos[1] <= max_y) & (new_pos[1] >= 0)
            if x_in and y_in:
                if self.matriz[new_pos[0]][new_pos[1]] == valor: 
                    resultado.append(Node(new_pos,node))
                        
        return resultado

    def teste_objetivo(self, pos_eval):
        if(self.sucessor(pos_eval,3)):
            return 1
        return 0
    
    def solucao(self,node):
        solution = []
        while node.parent != None:
            solution.append(node.position())
            node = node.parent

        return solution
        
class BFS(Maze):
    def __init__(self, pos_inicio, pos_fim, matriz,ordem):
        super().__init__(pos_inicio, pos_fim, matriz,ordem)
        self.percorrido = []
        self.lista = []
        self.pos_atual = Node(pos = self.pos_inicio, parent = None)
        self.lista.append(self.pos_atual)

    def acao(self):
        done = False       
        
        self.pos_atual = self.lista.pop(0)
        self.percorrido.append(self.pos_atual)
            
        for i in self.sucessor(self.pos_atual,1):
            if i not in self.percorrido:
                self.lista.append(i)
                if self.teste_objetivo(i):
                    done = True
                    return self.solucao(i), done

        return [], done
    
class DFS(Maze):
    def __init__(self, pos_inicio, pos_fim, matriz, ordem):
        super().__init__(pos_inicio, pos_fim, matriz,ordem)
        self.percorrido = []
        self.lista_interjucoes = []
        self.pos_atual = Node(pos = self.pos_inicio, parent = None)
        self.percorrido.append(self.pos_atual)
        
    def acao(self):
        done = False
        self.pos_atual = self.percorrido[-1]
        
        sucessores = self.sucessor(self.pos_atual,1)
        if len(sucessores) > 1:
            self.lista_interjucoes.append(sucessores)
        else:
            if len(sucessores) == 0:
                sucessores = self.lista_interjucoes.pop()
        i = sucessores.pop()
            
        if sucessores not in self.percorrido:
            self.percorrido.append(i)
            if self.teste_objetivo(i):
                done = True
                return self.solucao(i), done
        
        return [], done

if __name__ == "__main__":
    
  condicao = input("Digite 0 para DFS ou 1 para BFS: ")
  
  start_t0 = time.time()
 
 
  # parsing user input
  parser = argparse.ArgumentParser()
  parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
  parser.add_argument("--maze_file", help="filename (csv) of the maze to load.", default="maze_0.csv", type=str)
  args = parser.parse_args()

  address = "mazes/" + args.maze_file
  grid = np.genfromtxt(address, delimiter=',', dtype=int)
  num_rows = len(grid)
  num_columns = len(grid[0])

  # define start, define goal
  start_pos = (0,0)
  goal_pos = (num_rows-1, num_columns-1)
  
  grid_dim = (num_rows-1, num_columns-1)

  # define start and goal
  grid[0, 0] = 2
  grid[-1, -1] = 3

  if args.display == 1:
    # define the two colors of the grid RGB
    black = (0,0,0)
    white = (255, 255, 255)
    green = (50,205,50)
    red = (255,99,71)
    grey = (211,211,211)
    blue = (153,255,255)
    magenta = (255,0,255)

    idx_to_color = [black, white, green, red, blue, magenta]

    # set the height/width of each location on the grid
    height = 7
    width = height # i want the grid square
    margin = 1 # sets margin between grid locations

    # initialize pygame
    pygame.init()

    # congiguration of the window
    WINDOW_SIZE = [330, 330]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption(f"Pathfinder. Solving: {address}")

    # loop until done
    done = False
    run = False
    close = False

    clock = pygame.time.Clock() # to manage how fast the screen updates

    if condicao == "1":
        print("BFS!")
        solver = BFS(pos_inicio=start_pos, pos_fim=goal_pos, matriz=grid, ordem = grid_dim)
    else:
        print("DFS!")
        solver = DFS(pos_inicio=start_pos, pos_fim=goal_pos, matriz=grid, ordem = grid_dim)

    # main program
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            # wait for user to press any key to start    
            elif event.type == pygame.KEYDOWN:
                run = True
        
        screen.fill(grey) # fill background in grey
        
        for row in range(num_rows):
            for column in range(num_columns):
                color = idx_to_color[grid[row, column]]
                pygame.draw.rect(screen, color, 
                                  [(margin + width) * column + margin, 
                                  (margin + height) * row + margin,
                                  width, height])
        
        
        clock.tick(60) # set limit to 60 frames per second
        pygame.display.flip() # update screen
        
        if run == True:

            sleep(0.01)
            solution, done = solver.acao()
        
            explored = solver.percorrido

            for pos in explored:
                grid[pos.position()] = 4

        if done == True:
            for pos in solution:
                grid[pos] = 5

            grid[0, 0] = 2
            grid[-1, -1] = 3

            screen.fill(grey) # fill background in grey
        
            for row in range(num_rows):
                for column in range(num_columns):
                    color = idx_to_color[grid[row, column]]
                    pygame.draw.rect(screen, color, 
                                      [(margin + width) * column + margin, 
                                      (margin + height) * row + margin,
                                      width, height])
        
        
            clock.tick(60) # set limit to 60 frames per second
            pygame.display.flip() # update screen

            
    print("Solved! Click exit.")
    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            # wait for user to press any key to start    
            elif event.type == pygame.KEYDOWN:
                close = True
    pygame.quit()

  else:
    print(f"Pathfinder. solving: {address}")

    # loop until done
    done = False
    
    if condicao == 1:
        solver = BFS(pos_inicio=start_pos, pos_fim=goal_pos, matriz=grid, ordem = grid_dim)
    else:
        solver = DFS(pos_inicio=start_pos, pos_fim=goal_pos, matriz=grid, ordem = grid_dim)

    # main program
    while not done:
        solution, done = solver.acao()
        
        explored = solver.percorrido

        for pos in explored:
            grid[pos.position()] = 4

    # lets save result in csv
    for pos in solution:
        grid[pos.position()] = 5

    grid[0, 0] = 2
    grid[-1, -1] = 3


  # export maze to .csv file
  with open(f"mazes_solutions/solution_{args.maze_file}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(grid)

  print(f"--- finished {time.time()-start_t0:.3f} s---")
  exit(0)