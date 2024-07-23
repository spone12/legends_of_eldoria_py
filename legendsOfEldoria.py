import pygame as pg
import sys
from os import path

from Classes.tileMap import *
from Sprites.sprites import *
from gameSettings import *

from Classes.db import *
from Classes.debug import *
from Classes.hud import *
from Classes.selectionMenuWindow import *

class LegendsOfEldoria:

    isDialogWindow = False

    def __init__(self):
        # Initialization
        pg.init()
        pg.font.init()
        
        # Setting the screen height and width
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pg.time.Clock()

        pg.display.set_caption(GAME_TITLE)
        pg.key.set_repeat(500, 100)

        self.loadData()

    def loadData(self):
        self.map = TiledMap(self, path.join(GAME_FOLDER, 'Maps/startLocation.tmx'))
        self.mapImg = self.map.makeMap()
        self.mapRect = self.mapImg.get_rect()
        self.db = DB()
       
    # Initialize all variables and do all the setup for a new game
    def newGame(self):

        # Classes 
        self.debug = Debug(self)
        self.hud = HUD(self)
        self.dialogWindow = SelectionMenuWindow(self)

        # Sprites
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = None
        self.mapObjects = {'randomChest': []}

        # Map
        self.map.renderObjects()
        self.camera = Camera(self.map.width, self.map.height)

        # Variables
        self.drawDebug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        if self.isDialogWindow:
            self.dialogWindow.update()
        else:
            #self.allSprites.update()
            self.player.update()
            self.mobs.update(self.player)
            self.camera.update(self.player, True)

    def draw(self):

        if self.isDialogWindow:
            self.dialogWindow.openWindow()
        else:
            self.screen.blit(self.mapImg, self.camera.applyRect(self.mapRect))

            for sprite in self.allSprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

                if self.drawDebug:
                    pass

            if self.drawDebug:
                self.debug.obstacles()
                
            # HUD
            self.hud.drawPlayerHealth(self.screen, self.player.hp)
            self.hud.drawPlayerMana(self.screen, self.player.mp)

        pg.display.flip()

    # Catch all events here
    def events(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                # Quit game
                if event.key == pg.K_ESCAPE and not self.isDialogWindow:
                    self.quit()
                # Debug
                elif event.key == pg.K_F1:
                    self.drawDebug = not self.drawDebug
                # Action open any
                elif event.key == pg.K_e:
                    self.dialogWindow.checkOpenWindow(OPEN)
                # Open inventory
                elif event.key == pg.K_i:
                    self.dialogWindow.checkOpenWindow(INVENTORY_OPEN)

    def showStartScreen(self):
        pass

    def showGoScreen(self):
        pass

game = LegendsOfEldoria()
game.showStartScreen()

while True:
    game.newGame()
    game.run()
    game.showGoScreen()
