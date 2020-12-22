from .mode import Mode
import time
from displays import color_convert
import math

FrameRate = 20

class FourRow(Mode):
    changeRequest = False
    board = []
    chipsize = 2
    indicatorx = 0
    indicatorColor = (0,255, 0)
    player = 0 # 0, 1 (maybe more?)
    rowneeded = 4
    winchips = set()
    maxplayers = 2
    state = 'playing' # 'playing', 'animating', 'end'
    playerColors = [(0, 0, 30), (255, 0, 0), (255, 255, 0), (0, 255, 0)]

    def run(self):
        self.initBoard()
        self.indicatorx = math.floor(len(self.board[0]) / 2)
        self.draw()
        lasttime = self.wait()
        while(not self.stop):
            if(self.state == 'animating'):
                self.animate()
                self.changeRequest = True
            # if(self.changeRequest or self.state == 'end'):
            #     self.draw()
            #     self.changeRequest = False
            self.draw()
            lasttime = self.wait(lasttime)

    def draw(self):
        if(self.state == 'end'):
            for chip in self.winchips:
                x, y = chip
                color = tuple([math.floor(((math.sin(time.time()) + 1)/4 + 0.5)*x) for x in self.playerColors[self.board[y][x]]])
                for i in range(self.chipsize):
                    for j in range(self.chipsize):
                        self.display.drawPixel(x*self.chipsize+i, y*self.chipsize+j, color)
            return
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if(self.state == 'playing' and x == self.indicatorx):
                    continue
                if(self.board[y][x] == 0):
                    color = tuple([math.floor(c*(1 - ((x+y)%2)*0.5) * 0.4) for c in self.getBackgroundColor(x, y)])
                else:
                    color = self.playerColors[self.board[y][x]]
                for i in range(self.chipsize):
                    for j in range(self.chipsize):
                        self.display.drawPixel(x*self.chipsize + i, y*self.chipsize + j, color)
        if(self.state == 'playing'): # custom indicator
            # for x in range(max(0, self.indicatorx * self.chipsize - 1), min(self.indicatorx * self.chipsize+3,self.display.width)):
            #     self.display.drawPixel(x, 0, self.indicatorColor)
            # for x in range(max(0, self.indicatorx * self.chipsize), min(self.indicatorx * self.chipsize+2,self.display.width)):
            #     self.display.drawPixel(x, 1, self.indicatorColor)
            for y in range(0, len(self.board)):
                if(self.board[y][self.indicatorx] == 0):
                    for i in range(self.chipsize):
                        for j in range(self.chipsize):
                            self.display.drawPixel(self.indicatorx*self.chipsize + i, y*self.chipsize + j, tuple([math.floor(0.3*x) for x in self.indicatorColor]))


    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime

    def initBoard(self):
        self.board = []
        for y in range(math.floor(self.display.height / self.chipsize)):
            tmp = []
            for x in range(math.floor(self.display.width / self.chipsize)):
                tmp.append(0)
            self.board.append(tmp) 

    def handleDirection(self, direction, connection = 0):
        if(self.player == connection):
            if(direction == 'LEFT'):
                for x in range(self.indicatorx-1, -1, -1):
                    if(self.board[0][x] == 0):
                        self.indicatorx = x
                        break
            elif(direction == 'RIGHT'):
                for x in range(self.indicatorx+1, len(self.board[0])):
                    if(self.board[0][x] == 0):
                        self.indicatorx = x
                        break
            self.changeRequest = True
    
    def handleConfirm(self, connection = 0):
        if(self.player == connection and self.state == 'playing'):
            self.state = 'animating'
            self.board[0][self.indicatorx] = self.player + 1
            self.changeRequest = True

    def animate(self): # calculate all falling chips and apply physics to them
        end = True
        for y in range(len(self.board) - 1):
            for x in range(len(self.board[y])):
                if(self.board[y][x] != 0 and self.board[y+1][x] == 0):
                    self.board[y+1][x] = self.board[y][x]
                    self.board[y][x] = 0
                    end = False
            if(not end):
                break
        if(end):
            #replace indicator
            for x in range(self.indicatorx, -1, -1):
                    if(self.board[0][x] == 0):
                        self.indicatorx = x
                        break
            for x in range(self.indicatorx, len(self.board[0])):
                    if(self.board[0][x] == 0):
                        self.indicatorx = x
                        break
            self.state = self.checkState()
    
    def checkState(self):
        # horizontal
        for y in range(len(self.board)):
            self.winchips = set()
            for x in range(len(self.board[y]) - 1):
                self.winchips.add((x, y))
                if(self.board[y][x] == self.board[y][x+1] and self.board[y][x] != 0):
                    self.winchips.add((x+1, y))
                else: 
                    self.winchips = set()
                if(len(self.winchips) == self.rowneeded):
                    return 'end'

        # vertical
        for x in range(len(self.board[0])):
            self.winchips = set()
            for y in range(len(self.board) - 1):
                self.winchips.add((x, y))
                if(self.board[y][x] == self.board[y+1][x] and self.board[y][x] != 0):
                    self.winchips.add((x, y+1))
                else: 
                    self.winchips = set()
                if(len(self.winchips) == self.rowneeded):
                    return 'end'

        # diagonal
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                color = self.board[y][x]
                if(color == 0):
                    continue

                self.winchips = set()
                self.winchips.add((x, y))
                # right down
                for i in range(self.rowneeded):
                    if(y+i < len(self.board) and x+i < len(self.board[0]) and self.board[y+i][x+i] == color):
                        self.winchips.add((x+i, y+i))
                        if(i == self.rowneeded-1):
                            return 'end'
                    else:
                        break

                self.winchips = set()
                self.winchips.add((x, y))
                # left down
                for i in range(self.rowneeded + 1):
                    if(y+i < len(self.board) and x-i > 0 and self.board[y+i][x-i] == color):
                        self.winchips.add((x-i, y+i))
                        if(i == self.rowneeded-1):
                            return 'end'
                    else:
                        break

        self.player = (self.player + 1) % self.maxplayers
        return 'playing'

    def getBackgroundColor(self, x, y):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)

    def handleReturn(self):
        self.changeRequest = True

    def getName(self):
        return "4 in a row"