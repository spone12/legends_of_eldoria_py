import pygame as pg
import pytmx
from gameSettings import *
from Sprites.sprites import *

class TiledMap:
    def __init__(self, game, filename) -> None:
        self.game = game

        tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tmx.width * tmx.tilewidth
        self.height = tmx.height * tmx.tileheight
        self.tmxData = tmx

    def render(self, surface):
        ti = self.tmxData.get_tile_image_by_gid

        for layer in self.tmxData.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)

                    if tile:
                        surface.blit(tile, 
                            (x * self.tmxData.tilewidth,
                            y * self.tmxData.tileheight)
                        )
    
    def makeMap(self):
        tempSurface = pg.Surface((self.width, self.height))
        self.render(tempSurface)
        return tempSurface
    
    def renderObjects(self):
        
        for tileObject in self.game.map.tmxData.objects:
            objCenter = pg.math.Vector2(tileObject.x + tileObject.width / 2,
                        tileObject.y + tileObject.height / 2)
            
            if tileObject.name == 'player':
                self.game.player = Player(self.game, objCenter.x, objCenter.y)
            if tileObject.name == 'enemy':
                Mob(self.game, objCenter.x, objCenter.y)
            if tileObject.name == 'wall':
                Obstacle(self.game, tileObject.x, tileObject.y,
                         tileObject.width, tileObject.height)

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
