from .mode import Mode
import time
from displays import color_convert
import math
import random
import numpy as np

FrameRate = 60

# converted/copied from toggledbits C code: https://github.com/toggledbits/MatrixFireFast/blob/master/MatrixFireFast/MatrixFireFast.ino
class Twinkle(Mode):
    board = [] # saves current direction (brighten or darken) and brightness
    color = 0
    probability = 0.01

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
        if(step % max(1, math.floor(50/self.speed)) != 0):
            return
        for y in range(self.display.height):
            for x in range(self.display.width):
                self.display.drawPixel(x, y, color_convert.HSVtoRGB(self.color, (1-(self.board[y][x][1]/2)), self.board[y][x][1]))

    def calc(self, step = 0):
        if(step % max(1, math.floor(50/self.speed)) != 0):
            return

        self.color = (self.color+(self.speed/10000))%1

        # brighten/darken current pixels
        for y in range(self.display.height):
            for x in range(self.display.width):
                if(self.board[y][x][0] == 1):
                    if(self.board[y][x][1] >= 1):
                        self.board[y][x] = (-1,1)
                    else:
                        self.board[y][x] = (1,min(1,self.board[y][x][1]+(0.7/self.size)))
                elif(self.board[y][x][0] == -1):
                    if(self.board[y][x][1] <= 0):
                        self.board[y][x] = (0,0)
                    else:
                        self.board[y][x] = (-1,max(0,self.board[y][x][1]-(0.7/self.size)))

        # set new pixels
        for y in range(self.display.height):
            for x in range(self.display.width):
                if(self.board[y][x][0] == 0 and random.random()<self.probability):
                    self.board[y][x] = (1,0)
        
        
    def initBoard(self):
        self.board = []
        for y in range(self.display.height):
            tmp = []
            for x in range(self.display.width):
                tmp.append((0,0))
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
        return "twinkle"
