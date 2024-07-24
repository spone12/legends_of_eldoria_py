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
            for nameObj in obj:
                for objI, name in enumerate(self.game.mapObjects[nameObj]):
                    for i, item in enumerate(name.items):
                        if i == itemId:
                            self.items.append(item)
                            del self.game.mapObjects[nameObj][objI].items[i]

        else:
            for nameObj in obj:
                for objId, objects in enumerate(self.game.mapObjects[nameObj]):

                    for i, item in enumerate(objects.items):
                        self.items.append(item)
                    del self.game.mapObjects[nameObj][objId].items
                    self.game.mapObjects[nameObj][objId].items = []

    def getItems(self):
        ''' Get all inventory items '''
        
        return self.items

    def getItemsByAttr(self, attr = 'name'): 
        ''' Get values inventory items by attribute '''

        return [getattr(item, attr) for item in self.items]
    
    def dropItem(self, itemId: int):
        ''' Drop item by index '''

        for i, item in enumerate(self.items):
            if i == itemId:
                del self.items[itemId]
                return True
        return False

    def useItem(self, itemId):
        ''' Use Item by index '''

        for i, item in enumerate(self.items):
            if i == itemId:
                item.useItem()
                del self.items[itemId]
                return True
        return False
        