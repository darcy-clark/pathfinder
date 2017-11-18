import math
import random
import time
import sys
from heapq import *

#Gameboard class 

class GameBoard:
    def __init__ (self,size):
        self.size = size
        self.wall = 'X'
        self.board = [[" " for i in range(size)] for j in range(size)] #initialize a blank board list of lists
        print("gameboard created")
        self.obstacle_list = [] #initialize empty list of obstacle_list
        self.make_obstacles()
　
    def clear_board(self):
        self.board = [[" " for i in range(self.size)] for j in range(self.size)]
　
    def make_obstacles(self):
    #makes square obstacle block
        for i in range(3,7):
         for j in range(3,7):
            self.obstacle_list.append((i,j))
            self.board[i][j] = self.wall
        
    def draw(self):
    #draws all char on CLI
        print ("\n" * 50)
        for i in range(self.size):
            for j in range(self.size):
                print("|" + str(self.board[i][j]), end = '')
            print('|')
        print ("")
        
#Utility class for A* algorithm for enemy
class a_star_util:  
    def __init__(self,gameboard):
      self.board = gameboard
　
    def a_star_search (self, start, goal):
　
      close_set = set()
      came_from = {}
      gscore = {start:0}
      fscore = {start:self.heuristic(start, goal)}
      oheap = []
　
      heappush(oheap, (fscore[start], start))
    
      while oheap:
　
        current = heappop(oheap)[1]
        
        if goal == current: #abs((current[0] - goal[0])%self.limit) <= 1 and abs((current[1]-goal[1])%self.limit) <= 1:
            data = []
            #print("player found")
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
　
        close_set.add(current)
        for neighbour in self.get_neighbour(current):
        
          tentative_g_score = gscore[current] + self.heuristic(current, neighbour)
          
          if (neighbour[1],neighbour[0]) in  self.board.obstacle_list:
              continue
          if neighbour in close_set and tentative_g_score >= gscore.get(neighbour, 0):
              continue
          if  tentative_g_score < gscore.get(neighbour, 0) or neighbour not in [i[1]for i in oheap]:
              came_from[neighbour] = current
              gscore[neighbour] = tentative_g_score
              fscore[neighbour] = tentative_g_score + self.heuristic(neighbour, goal)
              heappush(oheap, (fscore[neighbour], neighbour))
      return False
    
    def get_neighbour (self, block):
　
        x,y = block
        l = []
        l.append(((x-1)%self.board.size,y))
        l.append(((x+1)%self.board.size,y))
        l.append((x,(y-1)%self.board.size))
        l.append((x,(y+1)%self.board.size))
　
        return l
　
    def heuristic(self,a, b): #gets distance between a and b. Needs to be case specefic for wrap around board
　     
        x_d,y_d = 0,0
        if b[0] - a[0] > 0 :
            x_d = min(b[0] - a[0], (a[0]-b[0])%self.board.size)
        else:
            x_d = min(a[0] -b[0], (b[0]-a[0])%self.board.size)
        if b[1] - a[1] > 0 :
            y_d = min(b[1] - a[1], (a[1]-b[1])%self.board.size)
        else:
            y_d = min(a[1] -b[1], (b[1]-a[1])%self.board.size)
        
        return x_d**2 + y_d **2 
    
#default Char class for player/enemy　
class Char:
    def __init__ (self, char, pos, gameboard):
        self.char = char
        self.x = pos[0]
        self.y = pos[1]
        self.board = gameboard
        self.limit = gameboard.size
        self.util = a_star_util
    
    
    def is_clear(self, direction):
        
        if (direction == 'r'):
            if (self.y,((self.x + 1)%self.limit)) in self.board.obstacle_list:
                #print("not clear")
                return False 
        elif(direction == 'l'):
            if (self.y,((self.x - 1)%self.limit)) in self.board.obstacle_list:
                return False 
        elif(direction == 'd'):
            if (((self.y + 1)%self.limit),self.x) in self.board.obstacle_list:
                return False
        elif(direction == 'u'):
            if (((self.y - 1)%self.limit),self.x) in self.board.obstacle_list:
                return False
        else:
            return True
        return True
        
#Player class inherits Char
class Player(Char):
    def __init__ (self,char,pos, gameboard):
        Char.__init__(self,char,pos,gameboard)
        self.direction = 'r'
        self.direction_list = ['r','d','l','u']
        self.los = 2
  
    def see(self, e):
        for x in range(self.x-self.los,self.x+self.los+1):
            for y in range(self.y-self.los,self.y+self.los+1):
                if (x%self.limit,y%self.limit) == (e.x,e.y):
                    print ("enemy found")
                if (y%self.limit,x%self.limit) in self.board.obstacle_list:
                    #print('blocked at '+ str(y%self.limit)+','+str(x%self.limit))
                    pass
    def set_direction(self,direction):
        self.direction = direction
        
    def step (self):
        self.board.board[self.y][self.x] = " "
        
        if(self.is_clear(self.direction)):
            if self.direction == 'r':
                self.x = (self.x + 1)%self.limit
            elif self.direction == 'l':
                self.x = (self.x - 1)%self.limit
            elif self.direction == 'd':
                self.y = (self.y + 1)%self.limit
            elif self.direction == 'u':
                self.y = (self.y - 1)%self.limit
                
        self.board.board[self.y][self.x] = self.char
    
    def turn_right(self):
        self.direction = self.direction_list[(self.direction_list.index(self.direction)+1)%len(self.direction_list)]
    
    def turn_left(self):
        self.direction = self.direction_list[(self.direction_list.index(self.direction)-1)%len(self.direction_list)]
    
    def is_blocked(self):
        return not self.is_clear(self.direction)
        
    '''not used for now, used for players to eat up other obstacles'''
    def action (self, direction):
    
        if self.is_clear(direction) == False:
            if direction == 'r':
                self.board[self.y][(self.x+1)%self.limit] = " "
                #print((self.x,self.y))
                self.board.obstacle_list.remove((self.y,(self.x+1)%self.limit))
                
            if direction == 'l':
                self.board[self.y][(self.x-1)%self.limit] = " "
                #print((self.x,self.y))
                self.board.obstacle_list.remove((self.y,(self.x-1)%self.limit))
                
            if direction == 'd':
                self.board[(self.y+1)%self.limit][self.x] = " "
                #print((self.x,self.y))
                self.board.obstacle_list.remove(((self.y+1)%self.limit,self.x))
                
            if direction == 'u':
                self.board[(self.y-1)%self.limit][self.x] = " "
                #print((self.x,self.y))
                self.board.obstacle_list.remove(((self.y-1)%self.limit,self.x))
      
    def update(self,e_pos):
      ##this is where u code      
        self.step()
        if(self.is_blocked()):
            self.turn_right()
            
#Enemy class    
class Enemy(Char,a_star_util):
    def __init__ (self,char,pos,gameboard,player):
        Char.__init__(self,char,pos,gameboard)
        a_star_util.__init__(self,gameboard)
        
    def set_position(self,pos):
        self.board.board[self.y][self.x] = " "
        self.x = pos[0]
        self.y = pos[1]
        self.board.board[self.y][self.x] = self.char
　
    def update (self, player_pos):
      try:
          self.set_position(self.a_star_search((self.x,self.y),(player_pos[0],player_pos[1]))[-1])
      except:
          pass
      if (self.x,self.y) == (player_pos[0],player_pos[1]):
          print ("game over")
          return False
      return True
      
class Game:
    def __init__(self, player_fps, enemy_fps):
        self.player_fps = player_fps
        self.enemy_fps = enemy_fps
        self.board = GameBoard(20)
        self.board.make_obstacles()
        
        self.player = Player('O',(0,0),self.board)
        self.enemy = Enemy('I',(10,10),self.board,self.player)
        self.board.draw()
        self.player_time = time.time()
        self.enemy_time = time.time()
        self.start_time = time.time()
    
    def run(self):
        loop = True
        while loop:
            if time.time() - self.player_time > self.player_fps:
                self.player.update((self.enemy.x,self.enemy.y))
                self.player_time = time.time()
                self.board.draw()
                
            if time.time() - self.enemy_time > self.enemy_fps:   
                if not self.enemy.update((self.player.x,self.player.y)):
                    loop = False
                self.enemy_time = time.time()
            if time.time() - self.start_time > 1:
                self.board.draw()
                self.start_time = time.time()
　
　
game = Game(1,2)
game.run()
