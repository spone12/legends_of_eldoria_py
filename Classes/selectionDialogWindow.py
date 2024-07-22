import math
import pygame as pg
from gameSettings import *

class SelectionDialogWindow():
    fontSize = 36
    fontColor = WHITE
    menuActions = ['Take', 'Test']
    
    def __init__(self, game):

        self.game = game
        self.font = pg.font.Font(None, self.fontSize)
        self.last_update = pg.time.get_ticks()  # Latest update time

        self.actions = []
        self.currentAction = 0
        self.activeAction = 0
        self.isUpperMenuActive = True  # Flag to track the active menu

    # Debug values or text on the screen
    def window(self, actions) -> None:
        self.actions = actions
        self.game.screen.fill(BLACK)

        # Top menu
        for i, action in enumerate(actions):
            color = LIGHTGREY
            if (self.isUpperMenuActive and i == self.currentAction) or (not self.isUpperMenuActive and i == self.activeAction):
                color = self.fontColor
                
            text = self.font.render(action, True, color)
            self.game.screen.blit(text, (100, 100 + i * 40))

        # Bottom menu
        for i, action in enumerate(self.menuActions):
            color = self.fontColor if i == self.currentAction and not self.isUpperMenuActive else LIGHTGREY
            text = self.font.render(action, True, color)
            self.game.screen.blit(text, (100 + i * 90, SCREEN_HEIGHT - 100))

    def keyPressButtons(self) -> None:
        keys = pg.key.get_pressed()
        if self.isUpperMenuActive:
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.currentAction = (self.currentAction - 1) % len(self.actions)
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.currentAction = (self.currentAction + 1) % len(self.actions)
            elif keys[pg.K_RETURN]:
                self.isUpperMenuActive = False  # Switching to the bottom menu
                self.activeAction = self.currentAction
                self.currentAction = 0  # Reset the selection for the bottom menu
            elif keys[pg.K_ESCAPE]:
                self.game.isDialogWindow = not self.game.isDialogWindow
                self.menuReset()
        else:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.currentAction = (self.currentAction - 1) % len(self.menuActions)
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.currentAction = (self.currentAction + 1) % len(self.menuActions)
            elif keys[pg.K_RETURN]:
                self.action()
            elif keys[pg.K_ESCAPE]:
                self.isUpperMenuActive = True  # Return to top menu
                self.currentAction = self.activeAction

    def action(self) -> None:
        if self.isUpperMenuActive:
            # Actions for the top menu
            pass
        else:
            # Actions for the bottom menu
            pass

    def update(self) -> None:
        now = pg.time.get_ticks()
        if now - self.last_update > 80:
            self.last_update = now
            self.keyPressButtons()

    def checkOpenWindow(self, type):

        if type == INVENTORY_OPEN:
            self.game.isDialogWindow = not self.game.isDialogWindow
            self.menuReset()
            return True
        
        # Check open 
        elif type == OPEN:

            playerPos = pg.Vector2(self.game.player.rect.center)
            for chestObj in self.game.mapObjects['randomChest']:
                if playerPos.distance_to(chestObj.pos) < 30:
                    print(True)
    
    def menuReset(self) -> None:
        self.currentAction = 0
        self.activeAction = 0
        self.isUpperMenuActive = True
