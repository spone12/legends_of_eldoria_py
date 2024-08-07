import math
import pygame as pg
from gameSettings import *
from Classes.Items.Item import *

class SelectionMenuWindow():
    fontSize = 36
    fontColor = WHITE
    menuActions = []
    
    def __init__(self, game):

        self.game = game
        self.font = pg.font.Font(None, self.fontSize)
        self.last_update = pg.time.get_ticks()  # Latest update time

        self.type = INVENTORY_OPEN
        self.mapObjName = []
        self.menuObjects = []
        self.currentAction = 0
        self.activeAction = 0
        self.isUpperMenuActive = True  # Flag to track the active menu

    def openWindow(self):
        ''' Open window '''

        self.window()

    def window(self) -> None:
        ''' Rendering of window elements '''

        self.game.screen.fill(BLACK)

        if self.type == INVENTORY_OPEN:
            text = 'INVENTORY'
        else:
            text = 'CHEST'

        if len(self.menuObjects) == 0:
           self.screenText(text + ' EMPTY', LIGHTGREY, 50, 30)      
        else:
            # Top menu
            for i, object in enumerate(self.menuObjects):
                color = LIGHTGREY
                if (self.isUpperMenuActive and i == self.currentAction) or (not self.isUpperMenuActive and i == self.activeAction):
                    color = self.fontColor
                
                self.screenText(object.name, color, 100, 100 + i * 40)

            # Bottom menu
            for i, action in enumerate(self.menuActions):
                color = self.fontColor if i == self.currentAction and not self.isUpperMenuActive else LIGHTGREY
                self.screenText(action, color, 100 + i * 90,  SCREEN_HEIGHT - 100)
            
            self.screenText(text, LIGHTGREY, 50, 30)

            # Render item image
            self.game.screen.blit(self.menuObjects[self.activeAction].image, (SCREEN_WIDTH - 250, 150))

            # Render item effects
            for effect in self.menuObjects[self.activeAction].itemEffectActionTranscription():
                self.screenText(effect, self.fontColor, SCREEN_WIDTH - 350, 250 + i * 40)
            
    def screenText(self, text, color: str, x: int, y: int):
        ''' Render elements on window '''

        text = self.font.render(str(text), True, color)
        self.game.screen.blit(text, (x, y))

    def keyPressButtons(self) -> None:
        ''' Menu control '''
        
        keys = pg.key.get_pressed()

        if len(self.menuObjects) == 0 and not keys[pg.K_ESCAPE]:
            return False
        
        if self.isUpperMenuActive:
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.currentAction = (self.currentAction - 1) % len(self.menuObjects)
                self.activeAction = self.currentAction
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.currentAction = (self.currentAction + 1) % len(self.menuObjects)
                self.activeAction = self.currentAction
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
        ''' Actions '''

        if self.isUpperMenuActive:
            # Actions for the top menu
            pass
        else:
            # Actions for the bottom menu
            # Chest
            action = self.menuActions[self.currentAction]
            if self.type == OPEN:

                if self.mapObjName == []:
                    return False
                
                if action == 'Take':
                    self.game.player.inventory.addItems(self.mapObjName, self.activeAction)
                    self.checkOpenWindow(OPEN)
                    self.game.isDialogWindow = True
                if action == 'TakeAll':
                    self.game.player.inventory.addItems(self.mapObjName)
                    self.game.isDialogWindow = False

            # Inventory        
            elif self.type == INVENTORY_OPEN:
       
                if action == 'Use':
                    self.game.player.inventory.useItem(self.activeAction)
                if action == 'Drop':
                    self.game.player.inventory.dropItem(self.activeAction)
                    
                self.checkOpenWindow(INVENTORY_OPEN)
                self.game.isDialogWindow = True

    def update(self) -> None:
        ''' Update '''
        
        now = pg.time.get_ticks()
        if now - self.last_update > 80:
            self.last_update = now
            self.keyPressButtons()

    def checkOpenWindow(self, type):
        ''' Check window is open '''

        self.menuReset()
        isOpenWindow = False
        self.type = type

        if type == INVENTORY_OPEN:
            isOpenWindow =  True
            if len(self.game.player.inventory.items) > 0:
                self.menuObjects = self.game.player.inventory.getItems()

            self.menuActions = ['Use', 'Drop']
        
        # Check open 
        elif type == OPEN:

            playerPos = pg.Vector2(self.game.player.rect.center)
            for i, chestObj in enumerate(self.game.mapObjects['randomChest']):
                if playerPos.distance_to(chestObj.pos) < 30:

                    if not chestObj.isGeneratedItems:
                        chestObj.dropItems()
                    
                    isOpenWindow = True
                    self.menuActions = ['Take', 'TakeAll']
                    self.mapObjName = ['randomChest']

                    for item in chestObj.items:
                        self.menuObjects.append(item)

        if isOpenWindow:
            self.game.isDialogWindow = not self.game.isDialogWindow
    
    def menuReset(self) -> None:
        ''' Reset properties '''

        self.menuActions.clear()
        self.currentAction = 0
        self.activeAction = 0
        self.isUpperMenuActive = True
        self.mapObjName = []
        self.menuObjects = []
