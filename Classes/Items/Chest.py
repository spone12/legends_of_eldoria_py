import pygame as pg
import random, json
from gameSettings import *
from Classes.Items.Item import *


class Chest():
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.items = []
        self.maxDropItems = random.randint(0, 2)
        self.isGeneratedItems = False

    def dropItems(self):

        countItems = 0
        itemsData = self.game.db.get('items', random = True)
        for item in itemsData:
            if countItems > self.maxDropItems:
                break

            chanse = random.randint(0, 100)
            data = json.loads(item['data'])

            if chanse <= data['dropChance']:
                self.items.append(Item(self.game, item['data']))
                countItems += 1

        if len(self.items) == 0:
            self.items.append(EmptyItem(self.game))
        
        self.isGeneratedItems = True
