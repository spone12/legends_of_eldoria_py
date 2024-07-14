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
        gameFolder = path.dirname(__file__)
        imgFolder = path.join(gameFolder, 'Images')
        self.map = Map(path.join(gameFolder, 'Maps/map.txt'))

        self.PLAYER_IMAGES = {
            "up": pg.image.load(path.join(imgFolder, "Player/up.png")).convert_alpha(),
            "down": pg.image.load(path.join(imgFolder, "Player/down.png")).convert_alpha(),
            "left": pg.image.load(path.join(imgFolder, "Player/left.png")).convert_alpha(),
            "right": pg.image.load(path.join(imgFolder, "Player/right.png")).convert_alpha()
        }

         # Текущее направление игрока
        self.playerDirection = "up"
        self.playerImg = self.PLAYER_IMAGES[self.playerDirection]
       
    def newGame(self):

        # initialize all variables and do all the setup for a new game
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)

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
        self.camera.update(self.player)

    def drawGrid(self):

        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREEN_HEIGHT))

        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (SCREEN_WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.drawGrid()

        for sprite in self.allSprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

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
                        self.playerDirection = "left"
                        self.player.move(dx =- 1)
                        break
                    case pg.K_RIGHT:
                        self.playerDirection = "right"
                        self.player.move(dx = 1)
                        break
                    case pg.K_UP:
                        self.playerDirection = "up"
                        self.player.move(dy =- 1)
                        break
                    case pg.K_DOWN:
                        self.playerDirection = "down"
                        self.player.move(dy = 1)
                        break
        
        # Обновление изображения игрока
        self.player.image = self.PLAYER_IMAGES[self.playerDirection]

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
