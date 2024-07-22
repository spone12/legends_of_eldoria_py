import pygame as pg
from gameSettings import *
from Classes.Items.Items import *
from Classes.Items.jsonImport import *

class Chest():
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        #self.items = JsonImport(self.game, path.join(GAME_FOLDER, 'JsonData/items.json'))
