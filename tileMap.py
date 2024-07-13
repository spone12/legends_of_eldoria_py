import pygame as pg
from gameSettings import *

class Map:
    def __init__(self, filename) -> None:
        self.data = []

        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
    
        self.tileWidth = len(self.data[0])
        self.tileHeight = len(self.data)
        self.width = self.tileWidth * TILESIZE
        self.height = self.tileHeight * TILESIZE

class Camera:
    def __init__(self, width, height) -> None:
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def update(self, target, limitScrolling = False):
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)
        
        # Limit scrolling to map size
        if limitScrolling:
            x = min(0, x) # Left side
            x = max(-(self.width - SCREEN_WIDTH), x) # Right side

            y = min(0, y) # Top side
            y = max(-(self.height - SCREEN_HEIGHT), y) # Bottom side

        self.camera = pg.Rect(x, y, self.width, self.height)
