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
        self.obj = None
        self.actions = []
        self.currentAction = 0
        self.activeAction = 0
        self.isUpperMenuActive = True  # Flag to track the active menu

    def openWindow(self):
        ''' Open window '''

        self.window(self.actions)

    def window(self, actions) -> None:
        ''' Rendering of window elements '''

        self.actions = actions
        self.game.screen.fill(BLACK)

        # Top menu
        for i, action in enumerate(actions):
            color = LIGHTGREY
            if (self.isUpperMenuActive and i == self.currentAction) or (not self.isUpperMenuActive and i == self.activeAction):
                color = self.fontColor
            
            self.screenText(action, color, 100, 100 + i * 40)

        # Bottom menu
        for i, action in enumerate(self.menuActions):
            color = self.fontColor if i == self.currentAction and not self.isUpperMenuActive else LIGHTGREY
            self.screenText(action, color, 100 + i * 90,  SCREEN_HEIGHT - 100)
        
        if self.type == INVENTORY_OPEN:
            text = 'INVENTORY'
        else:
            text = 'CHEST'
        
        self.screenText(text, LIGHTGREY, 50, 30)

    def screenText(self, text, color: str, x: int, y: int):
        ''' Render elements on window '''

        text = self.font.render(str(text), True, color)
        self.game.screen.blit(text, (x, y))

    def keyPressButtons(self) -> None:
        ''' Menu control '''
        
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
        ''' Actions '''

        if self.isUpperMenuActive:
            # Actions for the top menu
            pass
        else:
            if self.obj == None:
                return False
            
            # Actions for the bottom menu
            if self.type == OPEN:
                action = self.menuActions[self.currentAction]
                
                if action == 'Take':
                    self.game.player.inventory.addItems(self.obj, self.activeAction)


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
            if len(self.game.player.inventory.items) == 0:
                self.actions.append(EmptyItem(self.game).name)
            else:
                self.actions = self.game.player.inventory.getItemsByAttr('name')

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
                    self.obj = chestObj

                    for item in chestObj.items:
                        self.actions.append(item.name)

        if isOpenWindow:
            self.game.isDialogWindow = not self.game.isDialogWindow
    
    def menuReset(self) -> None:
        ''' Reset properties '''

        self.actions = []
        self.menuActions.clear()
        self.currentAction = 0
        self.activeAction = 0
        self.isUpperMenuActive = True
        self.obj = None
