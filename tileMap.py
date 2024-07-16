import pygame as pg
import pytmx
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

class TiledMap:
    def __init__(self, filename) -> None:
        tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tmx.width * tmx.tilewidth
        self.height = tmx.height * tmx.tileheight
        self.tmxdata = tmx

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid

        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)

                    if tile:
                        surface.blit(tile, 
                            (x * self.tmxdata.tilewidth,
                            y * self.tmxdata.tileheight)
                        )
    
    def makeMap(self):
        tempSurface = pg.Surface((self.width, self.height))
        self.render(tempSurface)
        return tempSurface

class Camera:
    def __init__(self, width, height) -> None:
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def applyRect(self, rect):
        return rect.move(self.camera.topleft)
    
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
