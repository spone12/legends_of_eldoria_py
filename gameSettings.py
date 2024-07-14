# Game name
import pygame as pg
from os import path

GAME_TITLE = 'Legends of Eldoria'

# Screen width and height window
SCREEN_WIDTH = 1024 # 16 * 64 OR 32 * 32 OR 64 * 16
SCREEN_HEIGHT = 768 # 16 * 48 OR 32 * 24 OR 64 * 12

# FPS count
FPS = 60

#TILE
TILESIZE = 32
GRID_WIDTH = SCREEN_WIDTH / TILESIZE
GRID_HEIGHT = SCREEN_HEIGHT / TILESIZE

# Folders
GAME_FOLDER = path.dirname(__file__)
IMG_FOLDER = path.join(GAME_FOLDER, 'Images')

#Player settings
PLAYER_SPEED = 1
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

#BG
BGCOLOR = BROWN
