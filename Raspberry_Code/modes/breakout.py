from .mode import Mode
import time
from displays import color_convert
import math
import random

FrameRate = 60

class Breakout(Mode):
    vel = (0,0) # velocity is vector that determines direction and speed
    ismoving = False
    platformwidth = 5
    position = 0
    bricks = [] # bricks are lists of coordinates

    def run(self):
        self.initField()
        lasttime = self.wait()
        i = 0
        while(not self.stop):
            self.draw()
            self.calc(i)
            lasttime = self.wait(lasttime)
            i += 1

    def draw(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                # draw field, ball, platform
                pass
    
    def calc(self, step):
        # move ball and calculate destroyed bricks etc
        # speed according to step
        pass

    def initField(self):
        # build Bricks
        # set Ball on platform
        # 

        pass


    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime

    def handleModeSetting(self, t):
        if('position' in t):
            self.position = min(math.floor(t['position'] * self.display.width / 100), self.display.width - self.platformwidth)

    def handleDirection(self, direction, connection = 0):
        if(direction == 'LEFT'):
            self.position = max(0, self.position - 1)
        elif(direction == 'RIGHT'):
            self.position = min(self.display.width - self.platformwidth, self.position + 1)
    
    def handleConfirm(self, connection = 0):
        # shoot ball from platform
        self.ismoving = True

    def handleReturn(self):
        pass

    def getBackgroundColor(self, x, y):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.3)

    def getName(self):
        return "breakout"