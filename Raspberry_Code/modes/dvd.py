from .mode import Mode
import time
from displays import color_convert
import json
import math
import random
FrameRate = 60

class DVD(Mode):
    changeRequest = False
    pointnumber = 3
    points = []
    trails = []
    vels = []
    size = 20
    pointstyle = "rainbow"
    pointcolor0 = (255, 255, 255, 255)
    pointcolor1 = (255, 255, 255, 255)
    backgroundstyle = "rainbow"
    backgroundcolor0 = (0, 0, 0, 255)
    backgroundcolor1 = (0, 0, 0, 255)

    def run(self):
        lasttime = None
        for point in range(self.pointnumber):
            (x, y) = (math.floor(random.randint(0, self.display.width-1)), math.floor(random.randint(0, self.display.height-1)))
            self.points.append((x, y))
            tmp = []
            for i in range(self.size - 1):
                tmp.append((x, y))
            self.trails.append(tmp)
            self.vels.append(( ([-1,1][random.randint(0,1)])*(random.random() + 0.5)*self.speed / 60 ,   ([-1,1][random.randint(0,1)])*(random.random() + 0.5)*self.speed / 60))
        while(not self.stop):
            self.draw()
            self.calc()
            self.changeRequest = False
            lasttime = self.wait(lasttime)
    
    def draw(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                ispoint = False
                for point in range(self.pointnumber):
                    if((x, y) in self.trails[point]):
                        self.display.drawPixel(x, y, self.getPointColor(x, y, self.trails[point].index((x, y)), point))
                        ispoint = True
                        break
                if(not ispoint):
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))

    def calc(self):
        for point in range(self.pointnumber):
            (x, y) = self.points[point]
            (xvel, yvel) = self.vels[point]
            (tmpx, tmpy) = (x, y)
            x += xvel
            y += yvel

            self.points[point] = (x, y)
            
            if(math.floor(tmpx) != math.floor(x) or math.floor(tmpy) != math.floor(y)):
                self.trails[point].pop()
                self.trails[point].insert(0, (math.floor(x), math.floor(y)))

            if(x >= self.display.width):
                xvel = -abs(xvel)
            if(y >= self.display.height):
                yvel = -abs(yvel)
            if(x <= 0):
                xvel = abs(xvel)
            if(y <= 0):
                yvel = abs(yvel)
            self.vels[point] = (xvel, yvel)

    def getPointColor(self, x, y, index = 0, pointnr = 0):
        opacity = 1 - (abs(self.size/3-index)/(self.size-self.size/3))
        if(self.pointstyle == 'solid'):
            return color_convert.MixColors(self.pointcolor0[:-1], self.getBackgroundColor(x, y), self.pointcolor0[-1] * opacity /255)
        if(self.pointstyle == 'fadeHorizontal'):
            length = self.display.width
            p = ((x + self.xpos)%length)/length
            frontcolor = color_convert.MixColors(self.pointcolor0, self.pointcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1] * opacity)
        if(self.pointstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            frontcolor = color_convert.MixColors(self.pointcolor0, self.pointcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1] * opacity)
        if(self.pointstyle == 'rainbow'):
            xpos = time.time()*0.05*(pointnr+1)%1
            size = 30/self.size
            (r, g, b) = color_convert.MixColors(color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1), self.getBackgroundColor(x, y), opacity)

        return (r, g, b)

    def getBackgroundColor(self, x, y):
        br0, bg0, bb0, ba0 = self.backgroundcolor0
        r = br0
        g = bg0
        b = bb0
        if(self.backgroundstyle == 'solid'):
            if(ba0 != 255):
                r = br0 * (ba0 / 255)
                b = bb0 * (ba0 / 255)
                g = bg0 * (ba0 / 255)
        if(self.backgroundstyle == 'fadeHorizontal'):
            length = self.display.width
            p = (x%length)/length
            r, g, b = color_convert.MixColors(self.backgroundcolor0[:-1], self.backgroundcolor1[:-1], p)
        if(self.backgroundstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            r, g, b = color_convert.MixColors(self.backgroundcolor0[:-1], self.backgroundcolor1[:-1], p)
        if(self.backgroundstyle == 'rainbow'):
            xpos = time.time()*0.01%1
            size = 20/self.size
            r, g, b = color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.3)
        return (r, g, b)


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
        self.changeRequest = True
    
    def handleConfirm(self):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True
    
    def handleModeSetting(self, t):
        tc = json.loads(t['pointcolor'])
        self.pointstyle = tc['style']
        self.pointcolor0 = self.getColorsFromMessage(tc['color0'])
        if(tc['style'] == 'fadeHorizontal' or tc['style'] == 'fadeVertical'):
            self.pointcolor1 = self.getColorsFromMessage(tc['color1'])
        bc = json.loads(t['backgroundcolor'])
        self.backgroundstyle = bc['style']
        self.backgroundcolor0 = self.getColorsFromMessage(bc['color0'])
        if(bc['style'] == 'fadeHorizontal' or bc['style'] == 'fadeVertical'):
            self.backgroundcolor1 = self.getColorsFromMessage(bc['color1'])

    def getName(self):
        return "dvd"