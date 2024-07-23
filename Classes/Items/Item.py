import pygame as pg
import json
from gameSettings import *

class Item():
    def __init__(self, game, data: str):

        self.game = game
        data = json.loads(data)
        self.itemKeys = data.keys()
        
        # Establish the properties of objects
        for k, v in data.items():
            setattr(self, k, v)

        # self.image = pg.Surface()

    def getItemProperties(self):
        for key in self.itemKeys:
            print(self.prop(key))

    def prop(self, prop):
        return getattr(self, prop)

class EmptyItem():
    def __init__(self, game):

        self.game = game
        self.name = 'Empty'
