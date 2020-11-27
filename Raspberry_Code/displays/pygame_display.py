import pygame
import sys
import threading
from pygame.locals import *
from .display import DisplayInterface
import math

class PYGameDisplay(DisplayInterface):
    def __init__(self, w, h):
        global DISPLAYSURF, SIZE
        super(PYGameDisplay, self).__init__(w, h)
        
        self.strip = []
        SIZE = 75

        pygame.init()
        pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.width*SIZE, self.height*SIZE))
        pygame.font.Font('freesansbold.ttf', 18)
        pygame.font.Font('freesansbold.ttf', 100)
        pygame.display.set_caption('PYGame Display')
        DISPLAYSURF.fill((  0,   0,   0))
        pygame.display.update()
        self.display_thread = threading._start_new_thread(self.run_display, ())

    def drawPixel(self, x, y, color):
        r, g, b = color
        pygame.draw.rect(DISPLAYSURF, (r*(self.brightness/100), g*(self.brightness/100), b*(self.brightness/100)), (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2), border_radius=SIZE)
        #pygame.draw.rect(DISPLAYSURF, (color>>16,(color>>8)&0xFF,color&0xFF), (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2), border_radius=SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        #pygame.display.update()
    
    def run_display(self): # call this in main process permanently
        global EXIT
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()