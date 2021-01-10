from .mode import Mode
import time
from displays import color_convert
import math
import random
import numpy as np

FrameRate = 60

# converted/copied from toggledbits C code: https://github.com/toggledbits/MatrixFireFast/blob/master/MatrixFireFast/MatrixFireFast.ino
class Rain(Mode):
    board = []
    colors = [
        [(0,0,0), (0,0,24), (0,0,64), (0,0,128), (0,0,170), (0,0,212), (50,0,255), (96,0,255), (128,0,255), (170,0,255), (212,0,255), ], # blue
        [(0,0,0), (24,0,0), (64,0,0), (128,0,0), (170,0,0), (212,0,0), (255,50,0), (255,96,0), (255,128,0), (255,170,0), (255,212,0), ], # red
        [(0,0,0), (0,24,0), (0,64,0), (0,128,0), (0,170,0), (0,212,0), (0,255,30), (0,255,96), (0,255,128), (0,255,170), (0,255,212), ]  # green
    ] # colors from colder to hotter
    color = 0
    probability = 0.03

    def run(self):
        lasttime = None
        self.initBoard()
        i = 0
        while(not self.stop):
            self.calc(i)
            self.draw(i)
            i+=1
            lasttime = self.wait(lasttime)

    def draw(self, step = 0): # make old point less appearant and blend new point in
        for y in range(self.display.height):
            for x in range(self.display.width):
                self.display.drawPixel(x, y, self.colors[self.color][math.floor(self.board[y][x])])

    def calc(self, step = 0):
        if(step % max(1, math.floor(50/self.speed)) != 0):
            return
        # shift everything down
        for y in range(len(self.board)-1, 0, -1):
            for x in range(len(self.board[y])):
                self.board[y][x] = self.board[y-1][x]

        # darken colors in top most row (shift color index by step (depending on self.size))
        for x in range(len(self.board[0])):
            self.board[0][x] = self.board[0][x]-(10/self.size)
            if(self.board[0][x] < 0):
                self.board[0][x] = 0

        # spawn new raindrops with some probability
        for x in range(len(self.board[0])):
            if(random.random() < self.probability):
                self.board[0][x] = random.randint(len(self.colors[self.color]) - 6, len(self.colors[self.color])-1)
        
        
    def initBoard(self):
        self.board = []
        for y in range(self.display.height):
            tmp = []
            for x in range(self.display.width):
                tmp.append(0)
            self.board.append(tmp)

    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime

    def handleDirection(self, direction, connection = 0):
        if(direction == 'UP'):
            self.probability = min(1, self.probability+0.005)
        elif(direction == 'DOWN'):
            self.probability = max(0, self.probability-0.005)
        elif(direction == 'RIGHT'):
            self.probability = min(1, self.probability+0.005)
        elif(direction == 'LEFT'):
            self.probability = max(0, self.probability-0.005)
    
    def handleConfirm(self, connection = 0):
        self.color = (self.color + 1) % len(self.colors)

    def handleReturn(self):
        pass

    def getName(self):
        return "rain"
