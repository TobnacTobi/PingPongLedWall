from .mode import Mode
import time
from displays import color_convert
import math
import random

changeAfterSeconds = 30
FrameRate = 60

class GameOfLife(Mode):
    x = y = 0 # position of point to flip a cell
    pointersize = 3
    board = []

    def run(self):
        lasttime = None
        self.x = math.floor(self.display.width / 2)
        self.y = math.floor(self.display.height / 2)
        self.initBoard()
        self.setRandomCells(0.50)
        i = 0
        while(not self.stop):
            if(i % math.floor(300/self.speed) == 0):
                self.calc()
                self.draw()
            if(self.changeRequest):
                self.draw()
                self.changeRequest = False
            i+=1
            lasttime = self.wait(lasttime)

    def draw(self): # make old point less appearant and blend new point in
        for y in range(self.display.height):
            for x in range(self.display.width):
                if(y >= self.y - self.pointersize/2 and y <= self.y + self.pointersize/2 and x >= self.x - self.pointersize/2 and x <= self.x + self.pointersize/2):
                    if(self.board[y][x]):
                        self.display.drawPixel(x, y, (255,255,0))
                    else:
                        self.display.drawPixel(x, y, (30,30,0))
                else:
                    if(self.board[y][x]):
                        self.display.drawPixel(x, y, self.getRainbowColor(-x, -y, 1))
                    else:
                        self.display.drawPixel(x, y, self.getRainbowColor(x, y, 0.3))

    def calc(self):
        newBoard = []
        for y in range(len(self.board)):
            tmp = []
            for x in range(len(self.board[y])):
                alive = self.getAliveNeighbours(x,y)
                if(self.board[y][x]):
                    tmp.append((alive == 2 or alive == 3))
                else:
                    tmp.append(alive == 3)
            newBoard.append(tmp)
        self.board = newBoard

    def getAliveNeighbours(self, xpos, ypos):
        count = 0
        for y in range(max(0, ypos-1), min(len(self.board), ypos+2)):
            for x in range(max(0, xpos-1), min(len(self.board[y]), xpos+2)):
                if((y != ypos or x != xpos) and self.board[y][x]):
                    count+=1
        return count

    def setRandomCells(self, probability):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if(random.random() < probability):
                    self.board[y][x] = True
    
    def initBoard(self):
        self.board = []
        for y in range(self.display.height):
            tmp = []
            for x in range(self.display.width):
                tmp.append(False)
            self.board.append(tmp)

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
    
    def handleConfirm(self, connection = 0):
        for y in range(max(0,math.floor(self.y-self.pointersize/2), min(len(self.board), math.floor(self.y+self.pointersize/2)))):
            for x in range(max(0,math.floor(self.x-self.pointersize/2), min(len(self.board[y]), math.floor(self.x+self.pointersize/2)))):
                #self.board[y][x] = not self.board[y][x]
                self.board[y][x] = True

    def handleReturn(self):
        self.changeRequest = True
    
    def getRainbowColor(self, x, y, brightness):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, brightness)

    def getName(self):
        return "Game of Life"