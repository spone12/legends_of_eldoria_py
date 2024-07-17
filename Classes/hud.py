import pygame as pg
from gameSettings import *

# HUD UI functions
class HUD():

    def __init__(self, game):
        pg.init()
        self.game = game
        self.font = pg.font.SysFont('Arial', 15)
    
    # Player health
    def drawPlayerHealth(self, surface, currentHp, x = 10, y = 10):
        
        pct = currentHp / PLAYER_HP
        if pct < 0:
            pct = 0

        fill = pct * BAR_LENGTH
        outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)

        pg.draw.rect(surface, RED, fillRect, 10, 40)
        pg.draw.rect(surface, WHITE, outlineRect, 2, 40)
        self.game.screen.blit(
            self.font.render(
                str(currentHp), True, WHITE
            ),
            (x + BAR_LENGTH / 2.2, y)
        )

    # Player mana
    def drawPlayerMana(self, surface, currentMana, x = 10, y = 35):
        
        pct = currentMana / PLAYER_MP
        fill = pct * BAR_LENGTH
        outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)

        pg.draw.rect(surface, BLUE, fillRect, 10, 40)
        pg.draw.rect(surface, WHITE, outlineRect, 2, 40)
        self.game.screen.blit(
            self.font.render(
                str(currentMana), True, WHITE
            ),
            (x + BAR_LENGTH / 2.1, y)
        )
