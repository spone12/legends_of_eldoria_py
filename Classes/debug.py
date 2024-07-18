import pygame as pg
from gameSettings import *

class Debug():

	fontSize = 18
	fontColor = WHITE
	
	def __init__(self, game):
		pg.init()
		self.game = game
		self.font = pg.font.SysFont('Arial', self.fontSize)

	# Debug values or text on the screen
	def text(self, info, y = 100, x = 10) -> None:
		
		debugSurf = self.font.render(str(info), True, WHITE)
		debugRect = debugSurf.get_rect(topleft = (x,y))
		pg.draw.rect(self.game.screen, BLACK, debugRect)
		self.game.screen.blit(debugSurf, debugRect)

	# Hit box 
	def hitRect(self) -> None:
		pass
	
	# FPS
	def fps(self):
		self.text("{:.2f}".format(self.game.clock.get_fps()), 10, SCREEN_WIDTH - 50)

	# Render obstacles
	def obstacles(self, fps = True) -> None:

		if fps:
			self.fps()

		for wall in self.game.walls:
			pg.draw.rect(self.game.screen, CYAN, self.game.camera.applyRect(wall.rect), 1)
			
	# Render grid
	def drawGrid(self) -> None:

		for x in range(0, SCREEN_WIDTH, TILESIZE):
			pg.draw.line(self.game.screen, LIGHTGREY, (x, 0), (x, SCREEN_HEIGHT))

		for y in range(0, SCREEN_HEIGHT, TILESIZE):
			pg.draw.line(self.game.screen, LIGHTGREY, (0, y), (SCREEN_WIDTH, y))
