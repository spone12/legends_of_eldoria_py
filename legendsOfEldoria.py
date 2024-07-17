import pygame as pg
import sys
from os import path

from tileMap import *
from Sprites.sprites import *
from gameSettings import *

from Classes.debug import *
from Classes.hud import *

class legendsOfEldoria:
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
        self.map = TiledMap(path.join(GAME_FOLDER, 'Maps/startLocation.tmx'))
        self.mapImg = self.map.makeMap()
        self.mapRect = self.mapImg.get_rect()
       
    def newGame(self):

        # initialize all variables and do all the setup for a new game
        self.debug = Debug(self)
        self.hud = HUD(self)
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()

        for tileObject in self.map.tmxData.objects:
            if tileObject.name == 'player':
                self.player = Player(self, tileObject.x, tileObject.y)
            if tileObject.name == 'enemy':
                Mob(self, tileObject.x, tileObject.y)
            if tileObject.name == 'wall':
                Obstacle(self, tileObject.x, tileObject.y,
                         tileObject.width, tileObject.height)

        self.camera = Camera(self.map.width, self.map.height)
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
        #self.allSprites.update()
        self.player.update()
        self.mobs.update(self.player)
        self.camera.update(self.player, True)

    def draw(self):
        
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

    def events(self):
        # catch all events here
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F1:
                    self.drawDebug = not self.drawDebug
        
        # Обновление изображения игрока
        self.player.image = self.player.PLAYER_IMAGES[self.player.direction]

    def showStartScreen(self):
        pass

    def showGoScreen(self):
        pass

game = legendsOfEldoria()
game.showStartScreen()

while True:
    game.newGame()
    game.run()
    game.showGoScreen()
