import pygame as pg
from gameSettings import *
from Classes.Items.Item import *

class Chest():
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.items = []

        itemsData = self.game.db.get('items', limit = 2)
        for item in itemsData:
            self.items.append(Item(self.game, item['data']))
