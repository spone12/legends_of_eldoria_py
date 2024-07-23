import pygame as pg
import json
from gameSettings import *

class Item():
    def __init__(self, game, data: str):

        self.game = game
        data = json.loads(data)
        
        # Establish the properties of objects
        for k, v in data.items():
            setattr(self, k, v)

        # self.image = pg.Surface()

        