import pygame as pg
from gameSettings import *
from Classes.Items.Items import *

class Chest():
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.items = {}
