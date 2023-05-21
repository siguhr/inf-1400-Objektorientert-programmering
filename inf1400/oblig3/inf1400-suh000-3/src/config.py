# -*- coding: utf-8 -*-
import pygame
from pygame import Vector2

#Colormap
WHITE = (255,255,255)
RED = (255,25,0)
BLACK = (0,0,0)
PINK = (255,15,219)
DARK_BLUE = (50, 88, 117)
BLUE = (0,0,255)


#Game window
SCREEN_X = 1000
SCREEN_Y = 700
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

#Globals
GAME_RUNNING = True
FPS = 60
COUNTERCLOCKWISE = 1
CLOCKWISE = -1
GRAVITY = 0.02
FUEL = 90

#Sizes
SPACESHIP_SIZE = (40, 40)
OBSTACLE_SIZE = (100, 100)
BASE_SURFACE_SIZE = (100, 5)
BULLET_SIZE = 4
BULLET_RADIUS = int(BULLET_SIZE/2)
BULLET_SURFACE_SIZE =  (BULLET_SIZE, BULLET_SIZE)
BULLET_SURFACE_CENTER = (BULLET_RADIUS, BULLET_RADIUS) 





#Obstacle positions   
POSITION_1 = (200, 300)
POSITION_2 = (700, 500)
POSITION_3 = (750, 150)
POSITION_4 = (500, 350)

#Images
spaceship_image = pygame.image.load("spaceship.png")
spaceship_image = spaceship_image.convert_alpha()
spaceship_image = pygame.transform.scale(spaceship_image, SPACESHIP_SIZE)