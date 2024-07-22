import pygame as pg
from gameSettings import *
import json

class Import():
    def __init__(self, game, file):
        self.game = game

        # Opening JSON file
        self.file = open(file)

    def loadFile(self):
        data = json.load(self.file)

        self.file.close()
        