import pygame as pg
from gameSettings import *

class Items(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.allSprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.type = type
        