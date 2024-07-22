import pygame as pg
from gameSettings import *

class Items():
    def __init__(self, game, pos, type):

        self.game = game
        self.image = pg.Surface()
        self.type = type
        