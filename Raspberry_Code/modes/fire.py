from .mode import Mode
import time
from displays import color_convert
import math
import random
import numpy as np

FrameRate = 60

# converted/copied from toggledbits C code: https://github.com/toggledbits/MatrixFireFast/blob/master/MatrixFireFast/MatrixFireFast.ino
class Fire(Mode):
    board = []
    colors = [
        [(0,0,0), (24,0,0), (64,0,0), (128,0,0), (170,0,0), (212,0,0), (255,50,0), (255,96,0), (255,128,0), (255,170,0), (255,212,0), (255,255,0), (255,255,30), (255,255,255)], # red
        [(0,0,0), (0,0,24), (0,0,64), (0,0,128), (0,0,170), (0,0,212), (50,0,255), (96,0,255), (128,0,255), (170,0,255), (212,0,255), (255,0,255), (255,30,255), (255,255,255)], # blue
        [(0,0,0), (0,24,0), (0,64,0), (0,128,0), (0,170,0), (0,212,0), (0,255,30), (0,255,96), (0,255,128), (0,255,170), (0,255,212), (0,255,255), (30,255,255), (255,255,255)]  # green
    ] # colors from colder to hotter
    color = 0
    nflare = 0
    maxflare = 8
    flarechance = 0.5
    flaredecay = 14
    flare = [(0,0,0)] * maxflare
    center = 0
    stepsize = 1

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
        for y in range(self.display.height):
            for x in range(self.display.width):
                self.display.drawPixel(x, y, self.colors[self.color][round(self.board[y][x])])

    def calc(self, step = 0):
        if(step % max(1, math.floor(50/self.speed)) != 0):
            return
        for y in range(len(self.board)-1):
            for x in range(len(self.board[0])):
                n = 0
                if(self.board[y+1][x] >= self.stepsize):
                    n = self.board[y+1][x] - self.stepsize
                self.board[y][x] = n
        for x in range(min(self.display.width, math.floor(step/(50/self.speed)))):
            self.board[len(self.board)-1][x] = max(random.randint(len(self.colors[self.color]) - 6, len(self.colors[self.color])-2) - math.floor(abs(self.display.width/2 - x)*self.center), 0)
        for i in range(self.nflare):
            x, y, z = self.flare[i]
            self.glow(x, y, z)
            if(z > 1):
                self.flare[i] = (x, y, z-1)
            else:
                for j in range(i+1, self.nflare):
                    self.flare[j-1] = self.flare[j]
                self.nflare-=1
        self.newFlare()
        
    def initBoard(self):
        self.board = []
        for y in range(self.display.height):
            tmp = []
            for x in range(self.display.width):
                tmp.append(0)
            self.board.append(tmp)

    def newFlare(self):
        if(self.nflare >= self.maxflare or random.random() >= self.flarechance):
            return
        x = random.randint(0,len(self.board[0])-1)
        y = random.randint(0,len(self.board)-1)
        z = len(self.colors)-1
        self.flare[self.nflare] = (x, y, z)
        self.nflare+=1
        self.glow(x,y,z)
    
    def glow(self, x,y,z):
        b = math.floor(z*10/self.flaredecay) + 1
        for i in range((y-b), (y+b)):
            for j in range((x-b), (x+b)):
                if(i < 0 or j < 0 or i >= len(self.board) or j >= len(self.board[0])):
                    return
                d = math.floor((self.flaredecay * math.sqrt((x-j)*(x-j) + (y-i)*(y-i)) + 5) / 10)
                n = 0
                if(z>d):
                    n = z-d
                if(n > self.board[i][j]): # color can only become brighter
                    self.board[i][j] = n

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
        if(direction == 'LEFT'):
            self.center = max(0,(self.center-0.1))
        elif(direction == 'RIGHT'):
            self.center = min(2,(self.center+0.1))
        elif(direction == 'UP'):
            self.stepsize = max(0, self.stepsize-0.1)
        elif(direction == 'DOWN'):
            self.stepsize = min(len(self.colors[self.color]), self.stepsize+0.1)
        self.flaredecay = math.floor(14 / ((self.stepsize + self.center*0.5)/1.5))
    
    def handleConfirm(self, connection = 0):
        self.color = (self.color + 1) % len(self.colors)

    def handleReturn(self):
        pass

    def getName(self):
        return "fire"
