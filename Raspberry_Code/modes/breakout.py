from .mode import Mode
import time
from displays import color_convert
import math
import random

FrameRate = 60

class Breakout(Mode):
    ismoving = False
    platformwidth = 5
    platformheight = 1
    position = 0
    vel = (0,0) # velocity is vector that determines direction and speed
    trail = [] # list of coordinates | head is point
    ball = (0,0)
    bricks = [] # bricks are lists of coordinates, width, color
    colors = [(50,0,255), (96,0,255), (128,0,255), (170,0,255), (212,0,255), (255,0,255)]

    ballstyle = "solid"
    ballcolor0 = (255, 255, 0, 255)
    ballcolor1 = (255, 255, 255, 255)
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
                isbrick = False
                for brick in self.bricks: # bricks
                    bx, by = brick[0]
                    if(x >= bx and y == by and x < bx + brick[1]):
                        self.display.drawPixel(x, y, self.colors[brick[2]])
                        isbrick = True
                        break
                if(isbrick):
                    continue
                if(y >= self.display.height - self.platformheight and x >= self.position and x < self.position + self.platformwidth): # platform
                    self.display.drawPixel(x, y, self.getPlatformColor(x, y))
                    break
                if((x, y) in self.trail): # trails
                    self.display.drawPixel(x, y, self.getBallColor(x, y, self.trail.index((x, y))))
                    continue

                self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
    
    def calc(self, step = 0):
        if(not self.ismoving):
            if(len(self.trail) > 1):
                self.trail.pop()
            return
        if(len(self.trail) > 5):
                self.trail.pop()

        tmpx, tmpy = self.ball
        x, y = self.ball
        (xvel, yvel) = self.vel
        x += xvel
        y += yvel

        if(math.floor(tmpx) != math.floor(x) or math.floor(tmpy) != math.floor(y)):
            self.trail.insert(0, (math.floor(x), math.floor(y)))

        #hits wall
        if(x >= self.display.width):
            xvel = -abs(xvel)
        if(y >= self.display.height):
            yvel = -abs(yvel)
        if(x <= 0):
            xvel = abs(xvel)
        if(y <= 0):
            yvel = abs(yvel)

        if(y >= self.display.height - self.platformheight and x >= self.position and x < self.position + self.platformwidth): # hits platform -> calculate new angle
            xvel = (x-self.position - (self.platformwidth/2)) / (self.platformwidth/2)
            yvel = -math.sqrt(1 - min(1, xvel*xvel))
            xvel*=(self.speed/50)
            yvel*=(self.speed/50)
        for i in range(len(self.bricks)):
            bx, by = self.bricks[i][0]
            (b, w, c) = self.bricks[i]
            if(x >= bx and math.floor(y) == by and x < bx + self.bricks[i][1]):
                if(self.bricks[i][2] <= 0):
                    self.bricks.pop(i)
                else:
                    self.bricks[i]=(b, w, c-1)
                if(abs(xvel) > abs(yvel)):
                    xvel = -xvel
                else:
                    yvel = -yvel
                break
        self.vel = (xvel, yvel)
        self.ball = (x, y)

    def initField(self):
        #build bricks
        for y in range(3):
            x = 0
            width = random.randint(2, 5)
            color = random.randint(0, len(self.colors)-1)
            while (x < self.display.width):
                self.bricks.append(((x, y), width, color))
                x+=width
                width = random.randint(2, 5)
                color = random.randint(0, len(self.colors)-1)
        # set ball on platform
        self.ball =  (self.position + random.randint(0,self.platformwidth-1), self.display.height - 1 - self.platformheight)
        self.trail.insert(0, (self.position + random.randint(0,self.platformwidth-1), self.display.height - 1 - self.platformheight))

    def getBallColor(self, x, y, index = 0, pointnr = 0):
        opacity = 1 - min(1, (index)/(self.size-self.size/3))
        if(self.ballstyle == 'solid'):
            return color_convert.MixColors(self.ballcolor0[:-1], self.getBackgroundColor(x, y), self.ballcolor0[-1] * opacity /255)
        if(self.ballstyle == 'fadeHorizontal'):
            length = self.display.width
            p = ((x + self.xpos)%length)/length
            frontcolor = color_convert.MixColors(self.ballcolor0, self.ballcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1] * opacity/255)
        if(self.ballstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            frontcolor = color_convert.MixColors(self.ballcolor0, self.ballcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1] * opacity/255)
        if(self.ballstyle == 'rainbow'):
            xpos = time.time()*0.05*(pointnr+1)%1
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
            r, g, b = color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.1)
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

    def handleModeSetting(self, t):
        if('position' in t):
            pos = min(math.floor(t['position'] * self.display.width / 100), self.display.width - self.platformwidth)

        if(not self.ismoving):
            offset = self.ball[0] - self.position
            self.ball = (pos + offset, self.ball[1])
            self.trail[0] = (pos + offset, self.trail[0][1])
        self.position = pos

    def handleDirection(self, direction, connection = 0):
        if(direction == 'LEFT'):
            pos = max(0, self.position - 1)
        elif(direction == 'RIGHT'):
            pos = min(self.display.width - self.platformwidth, self.position + 1)

        if(not self.ismoving):
            offset = self.ball[0] - self.position
            self.ball = (pos + offset, self.ball[1])
            self.trail[0] = (pos + offset, self.trail[0][1])
        self.position = pos
    
    def handleConfirm(self, connection = 0):
        if(not self.ismoving):
            xvel = (self.ball[0]-self.position - (self.platformwidth/2)) / (self.platformwidth)
            yvel = -math.sqrt(1 - (xvel*xvel))
            xvel*=(self.speed/50)
            yvel*=(self.speed/50)
            self.vel = (xvel, yvel)
        self.ismoving = True

    def handleReturn(self):
        pass

    def getBackgroundColor(self, x, y):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.3)

    def getName(self):
        return "breakout"