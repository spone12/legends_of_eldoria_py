import pygame as pg
import sys
from os import path

from tileMap import *
from Sprites.sprites import *
from gameSettings import *

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
        #self.map = Map(path.join(GAME_FOLDER, 'Maps/map.txt'))
        self.map = TiledMap(path.join(GAME_FOLDER, 'Maps/startLocation.tmx'))
        self.mapImg = self.map.makeMap()
        self.mapRect = self.mapImg.get_rect()
       
    def newGame(self):

        # initialize all variables and do all the setup for a new game
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)

        self.player = Player(self, 5, 5)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw(True)

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        #self.allSprites.update()
        self.player.update()
        self.mobs.update(self.player)
        self.camera.update(self.player, True)

    def drawGrid(self):

        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREEN_HEIGHT))

        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (SCREEN_WIDTH, y))

    def draw(self, debug = False):

        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.mapImg, self.camera.applyRect(self.mapRect))

        if debug: 
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            self.drawGrid()

        for sprite in self.allSprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # HUD
        self.player.drawPlayerHealth(self.screen, 10, 10, self.player.hp / PLAYER_HP)
        self.player.drawPlayerMana(self.screen, 10, 35, self.player.mp / PLAYER_MP)

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_ESCAPE:
                        self.quit()
                        break
                    case pg.K_LEFT:
                        self.player.direction = "left"
                        self.player.move(dx =- self.player.speed)
                        break
                    case pg.K_RIGHT:
                        self.player.direction = "right"
                        self.player.move(dx = self.player.speed)
                        break
                    case pg.K_UP:
                        self.player.direction = "up"
                        self.player.move(dy =- self.player.speed)
                        break
                    case pg.K_DOWN:
                        self.player.direction = "down"
                        self.player.move(dy = self.player.speed)
                        break
        
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
