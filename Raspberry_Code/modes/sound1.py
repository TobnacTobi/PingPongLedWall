from .mode import Mode
import time
from displays import color_convert
import math
import random

FrameRate = 60

class Sound1(Mode):
    changeRequest = True
    values = []

    def run(self):
        lasttime = None
        self.initValues()
        while(not self.stop):
            if(self.changeRequest):
                self.draw()
                self.changeRequest = False
            lasttime = self.wait(lasttime)

    def draw(self):
        for y in range(self.display.height):
            for x in range(self.display.width):
                if(self.values[x] >= self.display.height - y):
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
                else:
                    self.display.drawPixel(x, y, (0,0,0))


    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime
    
    def initValues(self):
        for x in range(self.display.width):
            self.values.append(random.randint(0,self.display.height-1))

    def handleModeSetting(self, t):
        if('values' in t):
            self.values = t['values']
        self.changeRequest = True

    def getBackgroundColor(self, x, y):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)

    def handleDirection(self, direction, connection = 0):
        self.changeRequest = True
    
    def handleConfirm(self, connection = 0):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True

    def getName(self):
        return "sound1"