import pygame, time, argparse, csv
import numpy as np
from time import sleep
from numpy.random import randint

class Maze:
    def __init__(self, pos_inicio, pos_fim, matriz,ordem):
        self.ordem = ordem
        self.matriz = matriz
        self.pos_inicio = pos_inicio
        self.pos_fim = pos_fim
    
    def sucessor(self,pos,valor):
        (y, x) = pos
        (max_y,max_x) = self.ordem 
        resultado = []

        for mov in [(1,0), (-1,0), (0,1), (0,-1)]:
            new_pos = (y+mov[0],x+mov[1])
            x_in = (new_pos[1] <= max_x) & (x >= 0) 
            y_in = (new_pos[0]) & (y >= 0)
        if x_in and y_in:
            if self.matriz[new_pos[0]][new_pos[1]] == valor: 
                resultado.append(new_pos)
                        
        return resultado

    def teste_objetivo(self, pos_eval):
        if(self.sucessor(pos_eval,3)):
            return 1
        return 0
        
class BFS(Maze):
    def __init__(self, pos_inicio, pos_fim, matriz,ordem):
        super().__init__(pos_inicio, pos_fim, matriz,ordem)
        self.percorrido = []
        self.lista = []
        self.pos_atual = self.pos_inicio
        self.lista.append(self.pos_inicio)

    def acao(self):
        aux = self.lista.pop(0)
        self.pos_atual = (aux[0],aux[1])
        self.percorrido.append(aux)
        done = False

        for i in self.sucessor(self.pos_atual,1):
            if i not in self.percorrido:
                self.lista.append(i)
                if self.teste_objetivo(i):
                    done = True
                    self.percorrido.append(i)
                    return self.percorrido, done

        return [], done
    

if __name__ == "__main__":
  start_t0 = time.time()

  # parsing user input
  # example: python bfs_pathfinder.py --display=True --maze_file=maze_1.csv
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

    pygame.display.set_caption(f"BFS Pathfinder. Solving: {address}")

    # loop until done
    done = False
    run = False
    close = False

    clock = pygame.time.Clock() # to manage how fast the screen updates

    bfs = BFS(pos_inicio=start_pos, pos_fim=goal_pos, matriz=grid, ordem = grid_dim)

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
            solution, done = bfs.acao()
        
            explored = bfs.percorrido

            for pos in explored:
                grid[pos[0], pos[1]] = 4

        if done == True:
            for pos in solution:
                grid[pos[0], pos[1]] = 5

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
    print(f"Pathfinder BFS. solving: {address}")

    # loop until done
    done = False
    bfs = BFS(pos_inicio=start_pos, pos_fim=goal_pos, matriz=grid)

    # main program
    while not done:
        solution, done = bfs.acao()
        
        explored = bfs.percorrido

        for pos in explored:
            grid[pos[0], pos[1]] = 4

    # lets save result in csv
    for pos in solution:
        grid[pos[0], pos[1]] = 5

    grid[0, 0] = 2
    grid[-1, -1] = 3


  # export maze to .csv file
  with open(f"mazes_solutions/bfs_{args.maze_file}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(grid)

  print(f"--- finished {time.time()-start_t0:.3f} s---")
  exit(0)