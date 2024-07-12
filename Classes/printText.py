import pygame
from gameSettings import *

#Print message class
class PrintText():

    fontType = 'effects//fonts//PingPong.ttf'
    fontColor = BLACK
    fontSize = 15

    def __init__(self, screen):
       self.screen = screen

    def print(
            self,
            message, 
            x = 50, 
            y = 100,
            fontSize = 15,
            color = fontColor
            ):

        fontTypeObj = pygame.font.Font(self.fontType, fontSize)
        text = fontTypeObj.render(str(message), True, color)
        self.screen.blit(text, (x, y))
        