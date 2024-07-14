import pygame as pg
from gameSettings import *

class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.PLAYER_IMAGES = {
            "up": pg.image.load(path.join(IMG_FOLDER, "Player/up.png")).convert_alpha(),
            "down": pg.image.load(path.join(IMG_FOLDER, "Player/down.png")).convert_alpha(),
            "left": pg.image.load(path.join(IMG_FOLDER, "Player/left.png")).convert_alpha(),
            "right": pg.image.load(path.join(IMG_FOLDER, "Player/right.png")).convert_alpha()
        }

        # initial character direction
        self.direction = 'up'
        self.image = self.PLAYER_IMAGES[self.direction]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):

        if not self.collideWithWalls(dx, dy):
            self.x += dx
            self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def collideWithWalls(self, dx = 0, dy = 0):

        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

class Wall(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
