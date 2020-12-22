from .mode import Mode
import time
from displays import color_convert
import math
import random

FrameRate = 60

class Snake(Mode):
    snakes = []
    vels = []
    dirs = [] # directions: 0=right,1=down,2=left,3=up
    colors = [(0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255)]
    foods = []
    foodcolor = (255, 0, 0)

    def run(self):
        self.snakes = []
        self.vels = []
        self.dirs = []
        self.addSnake()
        self.initFood()
        lasttime = self.wait()
        i = 0
        while(not self.stop):
            self.draw()
            self.calc(i)
            lasttime = self.wait(lasttime)
            if(self.changeRequest):
                self.setVels()
                self.changeRequest = False
            i += 1

    def draw(self):
        for x in range(self.display.width):
            for y in range(self.display.height):
                issnake = False
                for s in range(len(self.snakes)):
                    if((x, y) in self.snakes[s]):
                        self.display.drawPixel(x, y, self.colors[s])
                        issnake = True
                        break
                if(not issnake and (x, y) in self.foods):
                    self.display.drawPixel(x, y, self.foodcolor)
                    continue
                if(not issnake):
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
    
    def calc(self, step):
        for s in range(len(self.snakes)):
            if(step % math.floor(100/self.vels[s]) == 0):
                self.moveSnake(s)

    def setVels(self):
        for s in range(len(self.vels)):
            self.vels[s] = pow(math.floor(len(self.snakes[s])), 1.4)*self.speed/40 + self.speed

    def getFood(self):
        x = y = 0
        valid = False
        while(not valid):
            x = random.randint(0, self.display.width-1)
            y = random.randint(0, self.display.height-1)
            valid = not (x, y) in self.foods
            for snake in self.snakes:
                if((x, y) in snake):
                    valid = False
        return (x, y)

    def initFood(self):
        for i in range(4):
            self.foods.append(self.getFood())

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
        tmp = 0
        if(direction == 'LEFT'):
            tmp = 2
        elif(direction == 'RIGHT'):
            tmp = 0
        elif(direction == 'UP'):
            tmp = 3
        elif(direction == 'DOWN'):
            tmp = 1
        if((self.dirs[connection]%4) != ((tmp+2)%4) and self.dirs[connection] != tmp): # not in opposite direction
            self.dirs[connection] = tmp
            #self.moveSnake(connection)
    
    def handleConfirm(self, connection = 0):
        if(connection+1 > len(self.snakes) and (connection+1) < len(self.colors)):
            self.addSnake()

    def handleReturn(self):
        self.changeRequest = True

    def addSnake(self):
        tmp = []
        for s in range(4):
            tmp.append((math.floor(self.display.width/2) + s, math.floor(self.display.height/2)))
        self.snakes.append(tmp)
        self.vels.append(1)
        self.setVels()
        self.dirs.append(0)

    def getBackgroundColor(self, x, y):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.3)

    def moveSnake(self, s):
        x, y = self.snakes[s][0]
        if(self.dirs[s] == 0):
            x+=1
        elif(self.dirs[s] == 1):
            y+=1
        elif(self.dirs[s] == 2):
            x-=1
        elif(self.dirs[s] == 3):
            y-=1
        if(x < 0):
            x = self.display.width-1
        if(x > self.display.width-1):
            x = 0
        if(y < 0):
            y = self.display.height-1
        if(y > self.display.height-1):
            y = 0
        self.snakes[s].insert(0, (x, y))
        if((x, y) in self.foods):
            self.foods.remove((x, y))
            self.foods.append(self.getFood())
            self.setVels()
        else:
            self.snakes[s].pop()

    def getName(self):
        return "snake"