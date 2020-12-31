from .mode import Mode
import time
from displays import color_convert
from displays import texts
import math
import random

FrameRate = 60

class FlappyBird(Mode):
    pos = 0 # y pos of bird
    posx = 1 # x pos of bird
    birdsize = 2 # width and height from coordinate
    vel = 0 # y velocity of bird
    accel = 0.025 # y acceleration of bird per timestep
    ismoving = False
    pipewidth = 2
    pipeopening = (8,13) # min, max
    pipevel = 0 # x velocity of pipes
    pipes = [] # pipes have x coordinate + y coordinate (of opening) + size (of opening)
    score = 0

    birdstyle = "rainbow"
    birdcolor0 = (0, 0, 0, 255)
    birdcolor1 = (0, 0, 0, 255)
    pipestyle = "rainbow"
    pipecolor0 = (0, 0, 0, 255)
    pipecolor1 = (0, 0, 0, 255)
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
                ispipe = False
                for pipe in self.pipes:
                    if(x >= pipe[0] and x < pipe[0] + self.pipewidth and not (y >= pipe[1] and y < pipe[1] + pipe[2])):
                        self.display.drawPixel(x, y, self.getPipeColor(x, y))
                        ispipe = True
                if(ispipe):
                    continue
                if(x >= self.posx and x < self.posx + self.birdsize and y >= self.pos and y < self.pos + self.birdsize):
                    self.display.drawPixel(x, y, self.getBirdColor(x, y))
                    continue
                self.display.drawPixel(x, y, self.getBackgroundColor(x, y)) # draw background
    
    def calc(self, step = 0):
        if(not self.ismoving):
            return

        # move pipes (and replace) + count points
        if(step%math.floor(100/self.speed) == 0):
            for i in range(len(self.pipes)):
                (x, y, h) = self.pipes[i]
                x -= 1
                if(x + self.pipewidth < 0):
                    x = self.display.width
                    y = random.randint(0, self.display.height - self.pipeopening[0] - 1)
                    h = random.randint(self.pipeopening[0], self.pipeopening[1])
                self.pipes[i] = (x, y, h)
                if(x == self.posx):
                    self.score+=1

        # move bird
        self.pos += self.vel
        self.vel += self.accel

        if(self.pos <= 0):
            self.pos = 0
        if(self.vel > 0.4):
            self.vel = 0.4
        

        # check collision
        collision = False
        for pipe in self.pipes:
            if((self.posx <= pipe[0] + self.pipewidth and self.posx + self.birdsize > pipe[0]) and not (self.pos >= pipe[1] and self.pos + self.birdsize <= pipe[1] + pipe[2])):
                collision = True
        if(self.pos >= self.display.height):
            collision = True
        if(collision): # game over
            self.ismoving = False
            self.showScore()

    def initField(self):
        self.pipes = []
        offset = 10 # offset from pipe to pipe
        for p in range(math.floor(self.display.width / offset)):
            self.pipes.append(((p+1)*offset, random.randint(0, self.display.height - self.pipeopening[0] - 1), random.randint(self.pipeopening[0], self.pipeopening[1])))
        self.pos = math.floor(self.display.height / 2)

    def jump(self):
        self.vel = -0.25


    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime

        
    def getBirdColor(self, x, y):
        if(self.birdstyle == 'solid'):
            return color_convert.MixColors(self.birdcolor0[:-1], self.getBackgroundColor(x, y), self.birdcolor0[-1]/255)
        if(self.birdstyle == 'fadeHorizontal'):
            length = self.display.width
            p = ((x + self.xpos)%length)/length
            frontcolor = color_convert.MixColors(self.birdcolor0, self.birdcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1]/255)
        if(self.birdstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            frontcolor = color_convert.MixColors(self.birdcolor0, self.birdcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1]/255)
        if(self.birdstyle == 'rainbow'):
            xpos = time.time()*0.08%1
            size = 30/self.size
            (r, g, b) = color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)
        return (r, g, b)

    def getPipeColor(self, x, y):
        if(self.pipestyle == 'solid'):
            return color_convert.MixColors(self.pipecolor0[:-1], self.getBackgroundColor(x, y), self.pipecolor0[-1]/255)
        if(self.pipestyle == 'fadeHorizontal'):
            length = self.display.width
            p = ((x + self.xpos)%length)/length
            frontcolor = color_convert.MixColors(self.pipecolor0, self.pipecolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1]/255)
        if(self.pipestyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            frontcolor = color_convert.MixColors(self.pipecolor0, self.pipecolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1]/255)
        if(self.pipestyle == 'rainbow'):
            xpos = time.time()*0.05%1
            size = 10/self.size
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
            size = 10/self.size
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

    def handleModeSetting(self, t):
        if('position' in t):
            self.newvalues = min(math.floor(t['position'] * self.display.width / 100), self.display.width - self.platformwidth)

    def handleDirection(self, direction, connection = 0):
        pass
    
    def handleConfirm(self, connection = 0):
        if(not self.ismoving):
            self.ismoving = True
            return
        self.jump()

    def handleReturn(self):
        pass

    def getName(self):
        return "flappybird"