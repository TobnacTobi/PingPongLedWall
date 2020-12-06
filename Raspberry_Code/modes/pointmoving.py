from .mode import Mode
import time
from displays import color_convert
import math

changeAfterSeconds = 30
FrameRate = 60

class PointMoving(Mode):
    changeRequest = False
    x = xold = y = yold = 0

    def run(self):
        lasttime = None
        self.changeRequest = True

        self.x = math.floor(self.display.width / 2)
        self.xold = math.floor(self.display.width / 2)

        self.y = math.floor(self.display.height / 2)
        self.yold = math.floor(self.display.height / 2)
        while(not self.stop):
            if(self.changeRequest):
                self.display.clear()
                self.display.drawPixel(self.x, self.y, (255, 255, 255))
                # self.animatePoint()
                self.changeRequest = False
            lasttime = self.wait(lasttime)

    def animatePoint(self): # make old point less appearant and blend new point in
        steps = 7
        lasttime = None
        for i in range(steps+1):
            self.display.drawPixel(self.xold, self.yold, (25 * (steps-i), 25 * (steps-i), 25 * (steps-i)))
            self.display.drawPixel(self.x, self.y, (i * 255/steps, i * 255/steps, i * 255/steps))
            lasttime = self.wait(lasttime)
        self.display.drawPixel(self.x, self.y, (255, 255, 255))

    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime

    def handleDirection(self, direction):
        self.xold = self.x
        self.yold = self.y
        if(direction == 'LEFT'):
            self.x-=1
        elif(direction == 'RIGHT'):
            self.x+=1
        elif(direction == 'UP'):
            self.y-=1
        elif(direction == 'DOWN'):
            self.y+=1
        if(self.x < 0):
            self.x = 0
        if(self.x > self.display.width-1):
            self.x = self.display.width - 1
        if(self.y < 0):
            self.y = 0
        if(self.y > self.display.height-1):
            self.y = self.display.height - 1
        self.changeRequest = True
    
    def handleConfirm(self):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True

    def getName(self):
        return "pointmoving"