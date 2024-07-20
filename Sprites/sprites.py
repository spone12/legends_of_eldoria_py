import pygame as pg
import random
from gameSettings import *

def collideWithWalls(sprite, group, dx=0, dy=0):
    sprite.rect.x += dx #* TILESIZE
    sprite.rect.y += dy #* TILESIZE
    hit = pg.sprite.spritecollideany(sprite, group)
    sprite.rect.x -= dx #* TILESIZE
    sprite.rect.y -= dy #* TILESIZE
    return hit

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
        self.direction = 'up'
        self.image = self.PLAYER_IMAGES[self.direction]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

        self.hp = PLAYER_HP 
        self.mp = PLAYER_MP
        self.lvl = PLAYER_LVL
        self.speed = 3

    def keyPressButtons(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction = "left"
            self.move(dx =- self.speed)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction = "right"
            self.move(dx = self.speed)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction = "up"
            self.move(dy =- self.speed)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction = "down"
            self.move(dy = self.speed)
        
        # Updating the player's image
        self.image = self.PLAYER_IMAGES[self.direction]

    def move(self, dx=0, dy=0):
        if not collideWithWalls(self, self.game.walls, dx, dy):
            self.x += dx
            self.y += dy

    def update(self):
        self.keyPressButtons()
        self.rect.x = self.x #* TILESIZE
        self.rect.y = self.y #* TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.startingPos = (x, y)
        self.x = x
        self.y = y

        self.speed = 1  # Mob movement speed
        self.visibility_radius = 300  # Mob sight radius in tally
        self.hp = 20

    def move(self, dx=0, dy=0):
        if not collideWithWalls(self, self.game.walls, dx, dy):
            self.x += dx * self.speed
            self.y += dy * self.speed

    def can_see_player(self, player):
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        return distance <= self.visibility_radius

    def update(self, player):
        if self.can_see_player(player):
            direction_vector = pg.math.Vector2(player.x - self.x, player.y - self.y).normalize()
            self.move(direction_vector.x, direction_vector.y)
        else:
            self.return_to_starting_pos()
        
        if pg.sprite.collide_rect(self, player):
                self.handle_collision(player)
                
        self.rect.x = self.x
        self.rect.y = self.y
        
    def handle_collision(self, player):
        print("Collision with a player!")
        
    def return_to_starting_pos(self):
        if (self.x, self.y) != self.startingPos:
            direction_vector = pg.math.Vector2(self.startingPos[0] - self.x, self.startingPos[1] - self.y).normalize()
            self.move(direction_vector.x, direction_vector.y)

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
