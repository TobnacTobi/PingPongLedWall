from .mode import Mode
import time, threading
import datetime
from displays import color_convert
from displays import texts
from skimage.draw import line_aa
import numpy as np
import math
import json

FrameRate = 20

class ClockAnalog(Mode):
    hours = ""
    minutes = ""
    seconds = ""
    milliseconds = ""
    secondsFraction = 0 # fraction of whole led count to represent modulo seconds
    secondCountBrightness = 0.2
    countSeconds = True

    #length of hands (relative to clock size)
    hourlength = 0.5
    minutelength = 1
    secondlength = 1
    secondsColor = (255, 0, 255)
    minutesColor = (255, 255, 0)
    hoursColor = (0, 255, 255)
    handleMatrix = []

    textstyle = "solid"
    textcolor0 = (255, 255, 255, 255)
    textcolor1 = (255, 255, 255, 255)
    backgroundstyle = "rainbow"
    backgroundcolor0 = (0, 0, 0, 255)
    backgroundcolor1 = (0, 0, 0, 255)
    
    def run(self):
        self.xpos = math.floor((self.display.width)/2)
        self.ypos = math.floor((self.display.height)/2)
        while(not self.stop):
            timestr = str(datetime.datetime.now().time())
            self.hours = timestr[:2]
            self.minutes = timestr[3:5]
            self.seconds = timestr[6:8]
            self.milliseconds = timestr[9:14]
            self.secondsFraction = time.time() % (self.display.width * self.display.height)
            self.initMatrix()
            self.draw()

    def draw(self):
        cx = math.floor( self.display.width /2) # centerX
        cy = math.floor( self.display.height/2)# centerY
        length = math.floor(self.size*7/9)

        pSeconds = math.radians(math.floor((360*int(self.seconds)/60) - 90))
        pMinutes = math.radians(math.floor((360*int(self.minutes)/60) - 90))
        pHours = math.radians(math.floor((360*int(self.hours)/12) - 90))

        handlematrix = []
        for y in range(self.display.height):
            tmp = []
            for x in range(self.display.width):
                tmp.append(None)
            handlematrix.append(tmp)

        # include seconds
        destX = cx+ math.floor(length*self.secondlength*math.cos(pSeconds))
        destY = cy+ math.floor(length*self.secondlength*math.sin(pSeconds))
        self.drawLine(cx, cy, destX, destY, self.secondsColor)

        # include minutes
        destX = cx+ math.floor(length*self.minutelength*math.cos(pMinutes))
        destY = cy+ math.floor(length*self.minutelength*math.sin(pMinutes))
        self.drawLine(cx, cy, destX, destY, self.minutesColor)

        # include hours
        destX = cx+ math.floor(length*self.hourlength*math.cos(pHours))
        destY = cy+ math.floor(length*self.hourlength*math.sin(pHours))
        self.drawLine(cx, cy, destX, destY, self.hoursColor)

        for x in range(self.display.width):
            for y in range(self.display.height):
                if(math.floor(distance(x, y, cx, cy)) == length): # surrounding circle
                    self.display.drawPixel(x, y, self.textcolor0[:-1])
                elif(not (self.handleMatrix[y][x][0] == 0 and self.handleMatrix[y][x][1] == 0 and self.handleMatrix[y][x][2] == 0)): # handles
                    color = []
                    fcolor = tuple(self.handleMatrix[y][x])[:-1]
                    bgcolor = self.getBackgroundColor(x, y)
                    for i in range(len(fcolor)):
                        color.append(min(255, fcolor[i]+bgcolor[i]))
                    color = tuple(color)
                    self.display.drawPixel(x, y, color)
                else: # background
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
    
    def drawLine(self, x1, y1, x2, y2, color): # in handleMatrix
        rows, cols, weights = line_aa(y1, x1, y2, x2)    # antialias line
        w = weights.reshape([-1, 1])
        colorArray = []
        for c in color:
            colorArray.append(c)
        self.handleMatrix[rows, cols, 0:3] = (np.multiply((1 - w) * np.ones([1, 3]),  self.handleMatrix[rows, cols, 0:3]) + w * np.array([colorArray]))

    def initMatrix(self):
        self.handleMatrix = np.zeros((self.display.height, self.display.width, 4), dtype=np.uint8)
        self.handleMatrix[:,:,3] = 0

    def getTextColor(self, x, y, separator=False):
        tr0, tg0, tb0, ta0 = self.textcolor0
        tr1, tg1, tb1, ta1 = self.textcolor1
        if(separator):
            ta0=(ta0*self.separatoropacity)%256
        if(self.textstyle == 'solid'):
            if(ta0 == 255):
                return (tr0, tg0, tb0)
            return color_convert.MixColors(self.textcolor0[:-1], self.getBackgroundColor(x, y), ta0/255)
        if(self.textstyle == 'fadeHorizontal'):
            length = self.display.width
            p = ((x + self.xpos)%length)/length
            frontcolor = color_convert.MixColors(self.textcolor0, self.textcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1])
        if(self.textstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            frontcolor = color_convert.MixColors(self.textcolor0, self.textcolor1, p)
            return color_convert.MixColors(frontcolor[:-1], self.getBackgroundColor(x, y), frontcolor[-1])
        if(self.textstyle == 'rainbow'):
            xpos = time.time()*0.05%1
            size = 30/self.size
            (r, g, b) = color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)

        return (r, g, b)

    def getBackgroundColor(self, x, y):
        br0, bg0, bb0, ba0 = self.backgroundcolor0
        br1, bg1, bb1, ba1 = self.backgroundcolor1
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
            size = 5/self.size
            r, g, b = color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 0.5)

        # count seconds with pixels:
        if(self.countSeconds):
            d = (self.display.width * self.display.height)
            p = ((y * self.display.width + x - self.secondsFraction - 150) % d) / d
            if( p >= (1-1/d)):
                s = self.secondsFraction % 1
                r = math.floor(r * (self.secondCountBrightness + (s*(1-self.secondCountBrightness))))
                g = math.floor(g * (self.secondCountBrightness + (s*(1-self.secondCountBrightness))))
                b = math.floor(b * (self.secondCountBrightness + (s*(1-self.secondCountBrightness))))
            else:
                r = math.floor(r * (self.secondCountBrightness + (p*(1-self.secondCountBrightness))))
                g = math.floor(g * (self.secondCountBrightness + (p*(1-self.secondCountBrightness))))
                b = math.floor(b * (self.secondCountBrightness + (p*(1-self.secondCountBrightness))))
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
    
    def handleDirection(self, direction, connection = 0):
        self.changeRequest = True
    
    def handleConfirm(self, connection = 0):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True

    def handleModeSetting(self, t):
        tc = json.loads(t['textcolor'])
        self.textstyle = tc['style']
        print(self.textstyle)
        self.textcolor0 = self.getColorsFromMessage(tc['color0'])
        if(tc['style'] == 'fadeHorizontal' or tc['style'] == 'fadeVertical'):
            self.textcolor1 = self.getColorsFromMessage(tc['color1'])
        bc = json.loads(t['backgroundcolor'])
        self.backgroundstyle = bc['style']
        self.backgroundcolor0 = self.getColorsFromMessage(bc['color0'])
        if(bc['style'] == 'fadeHorizontal' or bc['style'] == 'fadeVertical'):
            self.backgroundcolor1 = self.getColorsFromMessage(bc['color1'])
        self.changeRequest = True
    
    def getColorsFromMessage(self, color):
        c = json.loads(color)
        return (c['r'], c['g'], c['b'], c['a'])

    def getName(self):
        return "clockanalog"

def distance(x1, y1, x2, y2):
    return (math.sqrt((x1-x2)**2 + (y1-y2)**2))
