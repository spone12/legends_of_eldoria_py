import pygame as pg
from gameSettings import *

class SelectionDialogWindow():

	fontSize = 36
	fontColor = WHITE
	
	def __init__(self, game):
		pg.init()
		self.game = game
		self.font = pg.font.Font(None, self.fontSize)
		self.last_update = pg.time.get_ticks()  # Latest update time

		self.actions = []
		self.currentAct = 1

	# Debug values or text on the screen
	def window(self, actions) -> None:

		self.actions = actions
		self.game.screen.fill((0, 0, 0))
		for i, action in enumerate(actions):
			color = self.fontColor if i == self.currentAct else LIGHTGREY
            
			text = self.font.render(action, True, color)
			self.game.screen.blit(text, (100, 100 + i * 40))
	
	def keyPressButtons(self) -> None:
		keys = pg.key.get_pressed()
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.currentAct = (self.currentAct - 1) % len (self.actions)
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.currentAct = (self.currentAct + 1) % len (self.actions)
		if keys[pg.K_RETURN]:
			self.action()

	def action(self):
		pass

	def update(self) -> None:
		now = pg.time.get_ticks()
		if now - self.last_update > 80:
			self.last_update = now
			self.keyPressButtons()
