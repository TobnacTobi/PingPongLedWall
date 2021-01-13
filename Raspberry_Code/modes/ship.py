from .mode import Mode
import time
from displays import color_convert
import math
import random
from opensimplex import OpenSimplex

FrameRate = 60

class Ship(Mode):
    ismoving = True
    platformwidth = 3
    position = 0
    walls = [] # 2D-array of boolean indicating where the wall is -> [y][x]
    holewidth = 6
    noise = None
    score = 0

    wallstyle = "solid"
    wallcolor0 = (0, 30, 255, 255)
    wallcolor1 = (255, 255, 255, 255)
    platformstyle = "solid"
    platformcolor0 = (255, 255, 255, 255)
    platformcolor1 = (255, 255, 255, 255)
    backgroundstyle = "rainbow"
    backgroundcolor0 = (0, 0, 0, 255)
    backgroundcolor1 = (0, 0, 0, 255)

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
                if(self.walls[y][x]):
                    self.display.drawPixel(x, y, self.getWallColor(x, y))
                elif((y >= self.display.height - 1 and x >= self.position and x < self.position + self.platformwidth) or (y >= self.display.height - 2 and x >= self.position + 1 and x < self.position + self.platformwidth -1)): # platform
                    self.display.drawPixel(x, y, self.getPlatformColor(x, y))
                else:
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
    
    def calc(self, step = 0):
        if(not self.ismoving or step%max(1, math.floor(50/self.speed)) != 0):
            return

        # shift row one down
        for y in range(len(self.walls)-1, 0, -1):
            for x in range(len(self.walls[y])):
                self.walls[y][x] = self.walls[y-1][x]

        # generate new wall row

        holepos = math.floor((((self.noise.noise2d(0, step/100)+1)/2)**2)*(self.display.width - self.holewidth))
        for x in range(len(self.walls[0])):
            self.walls[0][x] = True
        for x in range(self.holewidth):
            self.walls[0][x+holepos] = False

        # check for collision
        collision = False

        if(collision):
            self.showScore()
        self.score += 1

    def initField(self):
        # empty field
        self.noise = OpenSimplex(math.floor(random.random()*1000))
        self.walls = []
        for y in range(self.display.height):
            tmp = []
            for x in range(self.display.width):
                tmp.append(False)
            self.walls.append(tmp)


    def getWallColor(self, x, y):
        if(self.wallstyle == 'solid'):
            return color_convert.MixColors(self.wallcolor0[:-1], self.getBackgroundColor(x, y), self.wallcolor0[-1]/255)
        if(self.wallstyle == 'fadeHorizontal'):
            length = self.display.width
            p = ((x + self.xpos)%length)/length
            frontcolor = color_convert.MixColors(self.wallcolor0, self.wallcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1]/255)
        if(self.wallstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            frontcolor = color_convert.MixColors(self.wallcolor0, self.wallcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1]/255)
        if(self.wallstyle == 'rainbow'):
            xpos = time.time()*0.05%1
            size = 30/self.size
            (r, g, b) = color_convert.MixColors(color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1), self.getBackgroundColor(x, y), opacity)
        return (r, g, b)
    
    def getPlatformColor(self, x, y):
        if(self.platformstyle == 'solid'):
            return color_convert.MixColors(self.platformcolor0[:-1], self.getBackgroundColor(x, y), self.platformcolor0[-1]/255)
        if(self.platformstyle == 'fadeHorizontal'):
            length = self.display.width
            p = ((x + self.xpos)%length)/length
            frontcolor = color_convert.MixColors(self.platformcolor0, self.platformcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1])
        if(self.platformstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            frontcolor = color_convert.MixColors(self.platformcolor0, self.platformcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1])
        if(self.platformstyle == 'rainbow'):
            xpos = time.time()
            size = 30/self.size
            (r, g, b) = color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)
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

    def showScore(self):
        maxheight = self.display.height - 2
        textarr = texts.char_to_pixels(str(self.score)+"   ", fontsize=min(maxheight, self.size))
        #if(len(textarr[0]) - 2 <= self.display.width): # show short texts directly without moving animation
        #    self.displayText(textarr, 0)
        #    return
        framecount = 0
        lasttime = None
        xpos = 0
        while(not self.changeRequest and not self.stop):
            lasttime = self.wait(lasttime)
            framecount+=1
            if(framecount > 100/self.speed):
                framecount = 0
                xpos+=1
                self.displayText(textarr, xpos)

    def displayText(self, textarr, xpos):
        displayWidth = self.display.width
        displayHeight = self.display.height
        maxheight = self.display.height - 2
        y0 = math.floor((self.display.height - min(maxheight, self.size))/2)+2

        for x in range(displayWidth):
            for y in range(displayHeight):
                if(y >= y0 and y - y0 < len(textarr) and textarr[y - y0][(x + xpos)%len(textarr[y - y0])]): # draw text
                    self.display.drawPixel(x, y, (255,0,0))
                else: # draw background
                    ispipe = False
                    for pipe in self.pipes:
                        if(x >= pipe[0] and x < pipe[0] + self.pipewidth and not (y >= pipe[1] and y < pipe[1] + pipe[2])):
                            self.display.drawPixel(x, y, self.getPipeColor(x, y))
                            ispipe = True
                    if(ispipe):
                        continue
                    if(x >= self.posx and x < self.birdsize and y > self.pos and y < self.pos + self.birdsize):
                        self.display.drawPixel(x, y, self.getBirdColor(x, y))
                        continue
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y)) # draw background


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
            pos = min(math.floor(t['position'] * self.display.width / 100), self.display.width - self.platformwidth)
        self.position = pos

    def handleDirection(self, direction, connection = 0):
        if(direction == 'LEFT'):
            pos = max(0, self.position - 1)
        elif(direction == 'RIGHT'):
            pos = min(self.display.width - self.platformwidth, self.position + 1)
        self.position = pos
    
    def handleConfirm(self, connection = 0):
        self.ismoving = True

    def handleReturn(self):
        pass

    def getBackgroundColor(self, x, y):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.1)

    def getName(self):
        return "ship"