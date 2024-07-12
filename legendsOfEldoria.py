import pygame as pg
import sys

from Classes.printText import *

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
        pass
       
    def newGame(self):
        # initialize all variables and do all the setup for a new game
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, 10, 10)

        for x in range(10, 20):
            Wall(self, x, 5)

 
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
        self.allSprites.update()

    def drawGrid(self):

        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREEN_HEIGHT))

        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (SCREEN_WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        self.allSprites.draw(self.screen)
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
                        self.player.move(dx =- 1)
                        break
                    case pg.K_RIGHT:
                        self.player.move(dx = 1)
                        break
                    case pg.K_UP:
                        self.player.move(dy =- 1)
                        break
                    case pg.K_DOWN:
                        self.player.move(dy = 1)
                        break


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
