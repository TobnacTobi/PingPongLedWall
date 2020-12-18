from .mode import Mode
import time
from displays import color_convert
import math
import json

changeAfterSeconds = 30
FrameRate = 60

class Draw(Mode):
    changeRequest = True
    points = []

    def run(self):
        for x in range(self.display.width):
            tmpy = []
            for y in range(self.display.height):
                tmpy.append((0, 0, 0))
            self.points.append(tmpy)
        lasttime = self.wait()
        while(not self.stop):
            if(self.changeRequest):
                self.draw()
                self.changeRequest = False
            lasttime = self.wait(lasttime)

    def draw(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                self.display.drawPixel(x, y, self.points[x][y])

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
        if('point' in t):
            point = t['point']
            self.points[point[0]][point[1]] = (point[2], point[3], point[4])
            self.display.drawPixel(point[0], point[1], (point[2], point[3], point[4]))
        elif('points' in t):
            points = t['points']
            for x in range(self.display.width):
                tmpx = points[x]
                for y in range(self.display.height):
                    color = tmpx[y]
                    r = color[0]
                    g = color[1]
                    b = color[2]
                    self.points[x][y] = (r, g, b)
            self.changeRequest = True

    def handleDirection(self, direction):
        self.changeRequest = True
    
    def handleConfirm(self):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True

    def getName(self):
        return "draw"