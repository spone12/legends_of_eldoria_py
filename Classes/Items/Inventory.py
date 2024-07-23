import pygame as pg
from gameSettings import *
from Classes.Items.Item import *


class Inventory():
    ''' Player Inventory '''

    def __init__(self, game):
        self.game = game
        self.items = []
    
    def addItems(self, obj, itemId = None):
        ''' Add items to Inventory'''

        if itemId != None:
            for i, item in enumerate(obj.items):
                if i == itemId:
                    self.items.append(item)
        else:
            for item in obj.items:
                self.items.append(item)

    def getItems(self):
        ''' Get all inventory items '''
        return self.items

    def getItemsByAttr(self, attr = 'name'): 
        ''' Get values inventory items by attribute '''
        
        return [getattr(item, attr) for item in self.items]
