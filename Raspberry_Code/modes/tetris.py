from .mode import Mode
import time
from displays import color_convert
from displays import texts
import math
import random
import numpy

FrameRate = 60

class Tetris(Mode):
    board = []
    piece = None
    spawnpoint = (0,0)
    piecepos = (0,0) # position of the piece (top left corner of array)
    pieceColor = (255,255,255)
    state = 'playing' # playing, animating, end
    score = 0
    speed = 10

    def run(self):
        self.spawnpoint = (math.floor(self.display.width/2), 0)
        self.piecepos = self.spawnpoint
        self.initBoard()
        self.newPiece()
        lasttime = self.wait()
        i = 1
        while(not self.stop):
            if(self.state == 'end'):
                self.showScore()
            if(i % (60*7) == 0):
                self.speed+=1
            if(self.state == 'playing'):
                self.draw()
            if(i % math.floor(500/self.speed) == 0 and self.state != 'end' and self.state != 'animating'):
                self.calc(i)
            lasttime = self.wait(lasttime)
            i+=1

    def draw(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if(self.board[y][x] is None):
                    xpos, ypos = self.piecepos
                    if(y >= ypos and y-ypos < len(self.piece) and x >= xpos and x-xpos < len(self.piece[y-ypos]) and self.piece[y-ypos][x-xpos] == 1):
                        self.display.drawPixel(x, y, self.pieceColor)
                    else:
                        self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
                else:
                    self.display.drawPixel(x, y, self.board[y][x])
                        
    
    def calc(self, step = 0): # returns if piece was placed (True/False)
        if(self.isPieceEndPosition()):
            # add piece to board and spawn new piece | calculate any mutations in the board (rows vanishing)
            self.placePiece()

            #animation
            coordinates = []
            for y in range(len(self.piece)):
                for x in range(len(self.piece[y])):
                    if(self.piece[y][x] == 1):
                        coordinates.append((self.piecepos[0]+x, self.piecepos[1]+y))
            self.draw()
            self.animate(coordinates)
            #animation

            if(not self.isEnd()):
                self.newPiece()
                self.updateBoard()
            else:
                self.state = 'end'
            return True
        else:
            # move the piece 
            posx, posy = self.piecepos
            self.piecepos = (posx, posy+1)
            return False

    def initBoard(self):
        self.board = []
        for y in range(self.display.height):
            tmp = []
            for x in range(self.display.width):
                tmp.append(None)
            self.board.append(tmp)
        self.board = numpy.array(self.board)

    def handleDirection(self, direction, connection = 0):
        x, y = self.piecepos
        if(direction == 'LEFT'):
            if(self.checkPiecePosition((x-1, y))):
                x-=1
        elif(direction == 'RIGHT'):
            if(self.checkPiecePosition((x+1, y))):
                x+=1
        elif(direction == 'UP'):
            self.dropPiece()
            return
        elif(direction == 'DOWN'):
            self.calc()
            return
        self.piecepos = (x, y)
        self.keepPieceInsideScreen()
    
    def handleConfirm(self, connection = 0):
        self.rotatePiece()
        self.keepPieceInsideScreen()

    def handleReturn(self):
        self.changeRequest = True

    def placePiece(self):
        posx, posy = self.piecepos
        for y in range(len(self.piece)):
            for x in range(len(self.piece[y])):
                if(self.piece[y][x] == 1 and self.board[y+posy][posx+x] is None):
                    self.board[y+posy][posx+x] = self.pieceColor
    
    def dropPiece(self):
        wasPlaced = False
        while not wasPlaced:
            wasPlaced = self.calc()

    def isPieceEndPosition(self):
        posx, posy = self.piecepos
        for y in range(len(self.piece)):
            for x in range(len(self.piece[y])):
                if(self.piece[y][x] == 1 and (y+posy+1>=len(self.board) or (posx+x < len(self.board[y+posy+1]) and self.board[y+posy+1][posx+x] is not None))):
                    return True
        return False
    
    def checkPiecePosition(self, pos): # returns True if Piece position is ok
        xpos, ypos = pos
        for y in range(len(self.piece)):
            for x in range(len(self.piece[y])):
                if(self.piece[y][x] == 1 and y+ypos<len(self.board) and xpos+x < len(self.board[y+ypos]) and self.board[y+ypos][xpos+x] is not None):
                    return False
        return True


    def keepPieceInsideScreen(self):
        #do anything needed to keep piece inside screen (only visible parts of piece)
        posx, posy = self.piecepos
        for y in range(len(self.piece)):
            for x in range(len(self.piece[y])):
                if(self.piece[y][x] == 1):
                    if(posx + x < 0):
                        self.piecepos = ((posx-(posx + x)), posy)
                        return
                    elif(posx + x > len(self.board[0]) - 1):
                        self.piecepos = (posx-(posx + x - (len(self.board[0]) - 1)), posy)
                        return

    
    def rotatePiece(self):
        if(self.isPieceEndPosition()):
            return
        self.piece = numpy.rot90(self.piece)
        self.piece = numpy.rot90(self.piece)
        self.piece = numpy.rot90(self.piece)
    
    def newPiece(self):
        #create new piece and place it at spawnpoint
        pnr = random.randint(0,len(self.pieces)-1)
        self.pieceColor = self.colors[pnr]
        self.piece = self.pieces[pnr]
        self.piecepos = self.spawnpoint
    
    def updateBoard(self):
        for y in range(len(self.board)):
            curr = 0
            for x in range(len(self.board[y])):
                if(self.board[y][x] is None):
                    break
                else:
                    curr+=1
            if(curr >= len(self.board[y])):
                coordinates = []
                for x in range(len(self.board[y])):
                    coordinates.append((x, y))
                self.score += len(self.board[y])
                self.animate(coordinates)
                self.shiftBoard(y)           
                self.updateBoard()
                break
        
    def shiftBoard(self, row):
        for y in range(row, 0, -1):
            for x in range(len(self.board[y])):
                self.board[y][x] = self.board[y-1][x]

    def animate(self, coordinates = []):
        self.state = 'animating'
        steps = 20
        for i in range(steps):
            lasttime = self.wait()
            mult = (math.sin(i*(2*math.pi)/7) + 1)/4 + 0.5
            for c in coordinates:
                x, y = c
                self.display.drawPixel(x, y, tuple([math.floor((mult*c)) for c in self.board[y][x]]))
            lasttime = self.wait(lasttime)
        self.state = 'playing'
        
    def isEnd(self):
        for x in range(len(self.board[0])):
            if(self.board[0][x] is not None):
                return True
        return False


    def getBackgroundColor(self, x, y):
        xpos = time.time()*0.01%1
        size = 5/self.size
        return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.3)

    colors = [(0,255,255), (0,0,255),(255,127,80),(255,255,0),(0,255,0),(138,43,226),(255,0,0)]
    pieces = [
        [ # I
            [0,0,0,0],
            [1,1,1,1],
            [0,0,0,0],
            [0,0,0,0]
        ],
        [ # J
            [1,0,0],
            [1,1,1],
            [0,0,0]
        ],
        [ # L
            [0,0,1],
            [1,1,1],
            [0,0,0]
        ],
        [ # O
            [1,1],
            [1,1]
        ],
        [ # S
            [0,1,1],
            [1,1,0],
            [0,0,0]
        ],
        [ # T
            [0,1,0],
            [1,1,1],
            [0,0,0]
        ],
        [ # Z
            [1,1,0],
            [0,1,1],
            [0,0,0]
        ],
    ]

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
                    if(self.board[y][x] is not None):
                        self.display.drawPixel(x, y, tuple([math.floor(((math.sin(time.time()*(2*math.pi)) + 1)/4 + 0.5)*c) for c in self.board[y][x]]))
                    else:
                        self.display.drawPixel(x, y, self.getBackgroundColor(x, y))

    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime

    def getName(self):
        return "tetris"