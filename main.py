import time
import random
import sys
from maze_creator import main_maze
import os
import pygame
from pygame.locals import *
from pygame import mixer
from solved import path

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

#pygame initilization and basic settings...
pygame.init()

# setting up the clock
clock = pygame.time.Clock()

#music selection...
music_file_path = "sounds/"
music_file = []
for i in os.listdir(music_file_path):
    music_file.append(i)
music_f = random.choice(music_file)

surface = pygame.display.Info()
w, h = int(surface.current_w/40 ), int(surface.current_h/40 -1) 

# this creates maze from maze folder...
maze = main_maze(w, h)

#find maze solved:
maze_path = path(maze)

#pixel size for our sprites
pixel_size = 40

#game playing constant
playing = True
play_again = True
automate = False

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = len(maze[0])*pixel_size, len(maze)*pixel_size
BLACK = (0, 0, 0)
WHITE = (255,255,255)
text_color = (250, 105, 10)
won = False

# VARS:[would work as a main screen for our program...]
_VARS = {'surf': False}

#pygame basic settings
_VARS['surf'] = pygame.display.set_mode([SCREENSIZE[0], SCREENSIZE[1]], pygame.RESIZABLE)
pygame.display.set_caption('Mario Maze Game! - Developed by Jitu')

#music settings;
# start the mixer
mixer.init()
# loading the song
mixer.music.load(f"sounds/{music_f}")
# setting the volume
mixer.music.set_volume(0.6)
# start playing the song
mixer.music.play(-1)

#font settings;
# load the fonts 
font_30 = pygame.font.SysFont("Arial", 32, True, False)

#images being load;
wall = pygame.image.load("images/wall.png").convert()
player = pygame.image.load("images/mario1.png").convert()
flag = pygame.image.load('images/flag.png').convert()
skull = pygame.image.load('images/ghost.png').convert()

#find the start position
m = 0
for i in range(0, len(maze[0])):
    if maze[0][i] == 'O':
        m = i
        break

#find the exit block
exit_block = 0
for i in range(0, len(maze[0])):
    if maze[-1][i] == 'X':
        exit_block = i
        break

class Player:
    def __init__(self, x=0, y=0, index=0):
        self.x = x
        self.y = y
        self.index = [x/pixel_size, y/pixel_size]

    def draw_Player(self):
        _VARS['surf'].blit(player, (self.x, self.y))

    def move_up(self):
        if(self.collision(0, -1)):
            pass
        else:
            self.y -= pixel_size
            self.index = [self.x/pixel_size, self.y/pixel_size]
            
    def move_down(self):
        if(self.collision(0, 1)):
            pass
        else:
            self.y += pixel_size
            self.index = [self.x/pixel_size, self.y/pixel_size]
            
    def move_right(self):
        if(self.collision(1, 1)):
            pass
        else:
            self.x += pixel_size
            self.index = [self.x/pixel_size, self.y/pixel_size]
            
    def move_left(self):
        if(self.collision(1, -1)):
            pass
        else:
            self.x -= pixel_size
            self.index = [self.x/pixel_size, self.y/pixel_size]
        
    def collision(self, axis, direction):
        if(axis == 1):
            if (maze[int(self.index[1])][int(self.index[0]+direction)] == '#'):
                return True
            else:
                return False
        else:
            if(maze[int(self.index[1]+direction)][int(self.index[0])] == '#'):
                return True
            else:
                return False

    def check_won(self):
        global won
        if(int(self.index[0] == exit_block and int(self.index[1]) == len(maze)-1)):
            won = True
            self.y += 2*pixel_size
            _VARS['surf'].fill(BLACK)
            pygame.display.flip()
            pygame.time.delay(1000)
            pygame.quit()

    def automatic_play(self):
        _VARS['surf'].blit(skull, (self.x, self.y))
        automate = True
        self.x = m*pixel_size
        self.y = 0
        self.index = [self.x/pixel_size, self.y/pixel_size]
        _VARS['surf'].blit(player, (self.x, self.y))
        
        i = 0
        time_passed_since_last_iteration = 0
        
        while(i < len(maze_path)):
            dt = clock.tick()
            time_passed_since_last_iteration += dt

            if time_passed_since_last_iteration > 250:
                if maze_path[i] == "U":
                    self.y -= pixel_size
                    self.index = [self.x/pixel_size, self.y/pixel_size]
                    _VARS['surf'].blit(player, (self.x, self.y))
                elif maze_path[i] == "D":
                    self.y += pixel_size
                    self.index = [self.x/pixel_size, self.y/pixel_size]
                    _VARS['surf'].blit(player, (self.x, self.y))
                elif maze_path[i] == "L":
                    self.x -= pixel_size
                    self.index = [self.x/pixel_size, self.y/pixel_size]
                    _VARS['surf'].blit(player, (self.x, self.y))
                else:
                    self.x += pixel_size
                    self.index = [self.x/pixel_size, self.y/pixel_size]
                    _VARS['surf'].blit(player, (self.x, self.y))
                time_passed_since_last_iteration = 0
                i+=1
                pygame.display.flip()

p = Player(m*pixel_size , 0, m)

def main():
    run = True
    while run:
        checkEvents()
        _VARS['surf'].fill(BLACK)
        if(won == False ):
            drawStuffOnGrid()
            drawEndFlag()
            p.draw_Player()
            p.check_won()

        pygame.display.flip()
        clock.tick(60)

def drawEndFlag():
    _VARS['surf'].blit(flag, (exit_block*pixel_size, (len(maze)-1)*pixel_size))

def drawStuffOnGrid():
    x = 0
    y = 0

    for i in maze:
        for j in i:
            if j == '#':
                _VARS['surf'].blit(wall, (x*pixel_size, y*pixel_size))
            x += 1
            if x > len(maze[0])-1:
                x = 0
                y+= 1

def checkEvents():
    global play_again
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        key = pygame.key.get_pressed()
        if automate == False:
            if key[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if key[pygame.K_r]:
                play_again = True
            if key[pygame.K_a]:
                p.automatic_play()
            if key[pygame.K_LEFT]:
                p.move_left()
            if key[pygame.K_RIGHT]:
                p.move_right()
            if key[pygame.K_UP]:
                p.move_up()
            if key[pygame.K_DOWN]:
                p.move_down()
            
if __name__ == '__main__':
    main()
