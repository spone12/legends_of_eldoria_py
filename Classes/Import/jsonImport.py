import pygame as pg
from gameSettings import *
import json

class JsonImport():
    def __init__(self, game, file):
        self.game = game

        # Opening JSON file
        self.file = open(file)
        self.loadFile()

    def loadFile(self):
        self.data = json.load(self.file)
        self.file.close()

    # parse 'poisons.mana.small.mp'
    def parseByPath(self, path, tempData = None):
        
        if len(path) == 0:
            return tempData 
        
        if not tempData:
            tempData = self.data
        
        path = path.split('.')
        currentInd = path[0]
        del path[0]

        path = '.'.join(path)
        return self.parseByPath(path, tempData[currentInd])
        