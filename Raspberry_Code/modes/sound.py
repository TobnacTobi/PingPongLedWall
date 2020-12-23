from .mode import Mode
import time
from displays import color_convert
import math
import random
import numpy as np

FrameRate = 60

class Sound(Mode):
    changeRequest = True
    newvalues = [] # most recent values from app
    values = [] # smoothed values to display
    mode = 0
    modes = ['default', 'scroll', 'doubleside', 'visual1']

    # mode specific variables:
    #scroll
    scroll = []

    def run(self):
        lasttime = None
        self.initValues()
        i = 0
        while(not self.stop):
            self.calc(i)
            self.draw()
            #if(self.changeRequest):
            #    self.changeRequest = False
            i+=1
            lasttime = self.wait(lasttime)

    def calc(self, step = 0):
        for i in range(len(self.values)): # implies that len(newvalues) == len(values)
            if(self.newvalues[i] >= self.values[i]):
                self.values[i] = self.newvalues[i]
            else:
                self.values[i] = max(0, self.values[i]-0.4)

        if(self.modes[self.mode] == 'default'):
            pass
        elif(self.modes[self.mode] == 'scroll'):
            if(step% 2 != 0 ):
                return
            self.scroll = np.roll(self.scroll, -1, axis=0)
            for x in range(self.display.width):
                self.scroll[self.display.height-1][x] = self.getIntensityColor(self.newvalues[x])
        elif(self.modes[self.mode] == 'doubleside'):
            pass
        elif(self.modes[self.mode] == 'visual1'):
            pass

    def draw(self):
        for y in range(self.display.height):
            for x in range(self.display.width):
                if(self.modes[self.mode] == 'default'):
                    if(math.floor(self.values[x]) > self.display.height - y - 1):
                        self.display.drawPixel(x, y, self.getIntensityColor(self.display.height - y - 1))
                        #self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
                    elif(self.display.height - y - 1 == math.floor(self.values[x])):
                        self.display.drawPixel(x, y, (255,255,255))
                    else:
                        self.display.drawPixel(x, y, self.getBackgroundColor(-x, -y, 0.2))
                elif(self.modes[self.mode] == 'scroll'):
                    self.display.drawPixel(x, y, self.scroll[y][x])
                elif(self.modes[self.mode] == 'doubleside'):
                    if(math.floor(self.values[x]/2) >= abs(math.floor(self.display.height/2) - y)):
                        self.display.drawPixel(x, y, self.getIntensityColor(abs(self.display.height/2 - y)*2))
                    #elif(math.floor(self.values[x]/2) == abs(math.floor(self.display.height/2) - y)):
                    #    self.display.drawPixel(x, y, (255,255,255))
                    else:
                        self.display.drawPixel(x, y, self.getBackgroundColor(-x, -y, 0.2))


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
        self.values = []
        self.newvalues = []
        for x in range(self.display.width):
            self.values.append(random.randint(0,self.display.height-1))
            self.newvalues.append(0)

    def handleModeSetting(self, t):
        if('values' in t):
            self.newvalues = t['values']
        self.changeRequest = True

    def getBackgroundColor(self, x, y, brightness = 1):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, brightness)

    def getIntensityColor(self, v, max = 15, brightness = 1):
        degree = min(1.0, (2/3)-(v/max)*(2/3))
        return color_convert.HSVtoRGB(degree, 1, brightness)
    
    def initMode(self, m):
        if(self.modes[m] == 'default'):
            pass
        elif(self.modes[m] == 'scroll'):
            self.scroll = []
            for y in range(self.display.height):
                tmp = []
                for x in range(self.display.width):
                    tmp.append((0,0,0))
                self.scroll.append(tmp)
        elif(self.modes[m] == 'doubleside'):
            pass
        elif(self.modes[m] == 'visual1'):
            pass

    def handleDirection(self, direction, connection = 0):
        newmode = 0
        if(direction == 'LEFT'):
            newmode = (self.mode-1)%len(self.modes)
        elif(direction == 'RIGHT'):
            newmode = (self.mode+1)%len(self.modes)
        elif(direction == 'UP'):
           newmode = (self.mode+1)%len(self.modes)
        elif(direction == 'DOWN'):
            newmode = (self.mode-1)%len(self.modes)
        self.initMode(newmode)
        self.mode = newmode
    
    def handleConfirm(self, connection = 0):
        newmode = 0
        newmode = (self.mode+1)%len(self.modes)
        self.initMode(newmode)
        self.mode = newmode

    def handleReturn(self):
        self.changeRequest = True

    def getName(self):
        return "sound"