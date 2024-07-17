import pygame as pg
from gameSettings import *
pg.init()

class Debug():

	fontSize = 20
	fontType = pg.font.Font(None, fontSize)
	fontColor = BLACK
	
	def __init__(self, game):
		self.game = game

	# text on the screen
	def text(self, info, y = 10, x = 10) -> None:

		font = pg.font.Font(None,30)
		displaySurface = pg.display.get_surface()
		debugSurf = font.render(str(info), True, 'White')
		debugRect = debugSurf.get_rect(topleft = (x,y))
		pg.draw.rect(displaySurface, 'Black', debugRect)
		displaySurface.blit(debugSurf, debugRect)

	# hit box 
	def hitRect(self) -> None:
		pass
	
	# fps
	def fps(self):
		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

	# Render obstacles
	def obstacles(self) -> None:

		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		for wall in self.walls:
			pg.draw.rect(self.screen, CYAN, self.camera.applyRect(wall.rect), 1)
			
	# Render grid
	def drawGrid(self) -> None:

		for x in range(0, SCREEN_WIDTH, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREEN_HEIGHT))

		for y in range(0, SCREEN_HEIGHT, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (0, y), (SCREEN_WIDTH, y))
