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
        self.x = x
        self.y = y

        self.hp = PLAYER_HP 
        self.mp = PLAYER_MP
        self.lvl = PLAYER_LVL
        self.speed = 3

    def get_keys(self):
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

    # HUD functions
    def drawPlayerHealth(self, surface, x, y, pct):
        
        if pct < 0:
            pct = 0

        fill = pct * BAR_LENGTH
        outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)

        if pct > 0.6:
            color = DARK_GREEN
        elif pct > 0.3:
            color = YELLOW
        else:
            color = RED

        pg.draw.rect(surface, color, fillRect, 10, 40)
        pg.draw.rect(surface, WHITE, outlineRect, 2, 40)

    def drawPlayerMana(self, surface, x, y, pct):
        
        fill = pct * BAR_LENGTH
        outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)

        pg.draw.rect(surface, BLUE, fillRect, 10, 40)
        pg.draw.rect(surface, WHITE, outlineRect, 2, 40)

    def move(self, dx=0, dy=0):
        if not collideWithWalls(self, self.game.walls, dx, dy):
            self.x += dx
            self.y += dy

    def update(self):
        self.get_keys()
        self.rect.x = self.x #* TILESIZE
        self.rect.y = self.y #* TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.last_update = pg.time.get_ticks()  # Latest update time
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.change_direction_counter = 0

        self.speed = 10  # Mob movement speed (in pixels per step)
        self.visibility_radius = 5  #  Mob sight radius in tally
        self.hp = 20

    def move(self, dx=0, dy=0):
        if not collideWithWalls(self, self.game.walls, dx, dy):
            self.x += dx * self.speed
            self.y += dy * self.speed

    def can_see_player(self, player):
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        return distance <= self.visibility_radius

    def update(self, player):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:  # update every 500 ms
            self.last_update = now

            if self.can_see_player(player):
                dx, dy = 0, 0
                if self.x < player.x:
                    dx = 1
                elif self.x > player.x:
                    dx = -1
                if self.y < player.y:
                    dy = 1
                elif self.y > player.y:
                    dy = -1

                if dx != 0 and not collideWithWalls(self, self.game.walls, dx, 0):
                    self.move(dx=dx)
                elif dy != 0 and not collideWithWalls(self, self.game.walls, 0, dy):
                    self.move(dy=dy)
                else:
                    self.avoid_obstacle(dx, dy)
            else:
                self.random_move()

            if pg.sprite.collide_rect(self, player):
                self.handle_collision(player)

            self.rect.x = self.x #* TILESIZE
            self.rect.y = self.y #* TILESIZE

    def avoid_obstacle(self, dx, dy):
        # Алгоритм обхода препятствий
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Directions: right, left, down, up
        random.shuffle(directions)  # Shuffle directions for randomized traversal
        for direction in directions:
            new_dx, new_dy = direction
            if not collideWithWalls(self, self.game.walls, new_dx, new_dy):
                self.move(dx=new_dx, dy=new_dy)
                break

    def random_move(self):
        if self.change_direction_counter == 0:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.change_direction_counter = 60

        if self.direction == 'left' and not collideWithWalls(self, self.game.walls, -1, 0):
            self.move(dx=-1)
        elif self.direction == 'right' and not collideWithWalls(self, self.game.walls, 1, 0):
            self.move(dx=1)
        elif self.direction == 'up' and not collideWithWalls(self, self.game.walls, 0, -1):
            self.move(dy=-1)
        elif self.direction == 'down' and not collideWithWalls(self, self.game.walls, 0, 1):
            self.move(dy=1)
        else:
            self.change_direction_counter = 0  # Forced to change direction if it hits a wall

        self.change_direction_counter -= 1

    def handle_collision(self, player):
        print("Collision with a player!")

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
