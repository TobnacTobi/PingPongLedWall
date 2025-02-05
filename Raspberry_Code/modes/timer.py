from .mode import Mode
import time, threading
import datetime
from displays import color_convert
from displays import texts
import math
import json

FrameRate = 20

class Timer(Mode):
    state = "set" # set, run, alarm, off
    mode = "alarm" # alarm, off
    minutes = 3
    seconds = 0
    separator = ":"
    xpos = 0
    ypos = 0
    separatoropacity = 0.5
    countSeconds = True
    timerFraction = 0 # fraction of whole led count to represent fraction of timer
    timerCountBrightness = 0.4
    textstyle = "solid"
    textcolor0 = (255, 255, 255, 255)
    textcolor1 = (255, 255, 255, 255)
    backgroundstyle = "rainbow"
    backgroundcolor0 = (0, 0, 0, 255)
    backgroundcolor1 = (0, 0, 0, 255)
    
    def run(self):
        self.xpos = math.floor((self.display.width)/2)
        self.ypos = math.floor((self.display.height)/2)
        lasttimestr = str(datetime.datetime.now().time())
        while(not self.stop):
            self.separatoropacity = (math.sin(time.time()*math.pi)+1)/2
            self.timerFraction = time.time() % (self.display.width * self.display.height)
            self.getTextMatrix()
            self.showClock()
            if(self.state == "run"):
                timestr = str(datetime.datetime.now().time())
                seconds = timestr[6:8]
                lastseconds = lasttimestr[6:8]
                if(seconds != lastseconds):
                    self.tic()
                if(self.minutes == 0 and self.seconds == 0):
                    self.state = self.mode
                    continue
                lasttimestr = timestr
            elif(self.state == "off"):
                lasttime = None
                self.display.clear()
                while(not self.stop):
                    time.sleep(1)
            elif(self.state == "alarm"):
                self.display.setBrightness(((math.sin(time.time()*math.pi*4)+1)/2)*100)
                # make alarm
                pass
    
    def showClock(self):
        lasttime = None
        self.drawClock()
        lasttime = self.wait(lasttime)

    def drawClock(self):
        width = 0
        for a in self.clockarr:
            width += len(a[0])
        x0 = self.xpos - math.floor(width/2)
        y0 = self.ypos - math.floor(len(self.clockarr[0])/2)
        c = 0
        width = 0
        for x in range(self.display.width):
            for y in range(self.display.height):
                isText = False
                if(c < len(self.clockarr)):
                    if(y >= y0 and y - y0 < len(self.clockarr[c]) and
                        x >= x0 + width and x - x0 - width < len(self.clockarr[c][0]) and
                        self.clockarr[c][y - y0][x - x0 - width]):
                        if(c % 2 == 0):
                            self.display.drawPixel(x, y, self.getTextColor(x, y))
                        else:
                            self.display.drawPixel(x, y, self.getTextColor(x, y, True))
                        isText = True
                    if(y - y0 == len(self.clockarr[c])-1 and x - x0 - width == len(self.clockarr[c][0]) - 1):
                        width += len(self.clockarr[c][0])
                        c+=1
                        if(c < len(self.clockarr)):
                            y0 = self.ypos - math.floor(len(self.clockarr[c])/2)
                if(not isText): # draw background
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))
    
    def incTimer(self):
        self.seconds += 10
        if(self.seconds >= 60):
            self.seconds = (self.seconds % 60)
            self.minutes += 1
            self.minutes = min(self.minutes, 59)

    def decTimer(self):
        self.seconds -= 10
        if(self.seconds < 0):
            self.seconds = (self.seconds % 60)
            self.minutes -= 1
            self.minutes = max(self.minutes, 0)

    def tic(self):
        self.seconds -= 1
        if(self.seconds < 0):
            self.seconds = (self.seconds % 60)
            self.minutes -= 1
            self.minutes = max(self.minutes, 0)

    def getTextMatrix(self):
        maxheight = self.display.height - 2
        # hoursarr = texts.char_to_pixels(str(self.hours).zfill(2), fontsize=min(maxheight, math.floor(self.size/2)), path='./Raspberry_Code/displays/fonts/fffforward.ttf')
        minutesarr = texts.char_to_pixels(str(self.minutes).zfill(2), fontsize=min(maxheight, math.floor(self.size/2)), path='./Raspberry_Code/displays/fonts/fffforward.ttf')
        secondsarr = texts.char_to_pixels(str(self.seconds).zfill(2), fontsize=min(maxheight, math.floor(self.size/2)), path='./Raspberry_Code/displays/fonts/fffforward.ttf')
        # millisecondsarr = texts.char_to_pixels(self.milliseconds, fontsize=min(maxheight, math.floor(self.size/2)), path='./Raspberry_Code/displays/fonts/fffforward.ttf')
        separatorarr = self.getSeparator()
        # separatorarr = texts.char_to_pixels(self.separator, fontsize=min(maxheight, math.floor(self.size*3/4)), path='./Raspberry_Code/displays/fonts/fffforward.ttf')
        self.clockarr = []
        self.clockarr.append(minutesarr)
        self.clockarr.append(separatorarr)
        self.clockarr.append(secondsarr)
        # self.clockarr.append(separatorarr)
        # self.clockarr.append(millisecondsarr)

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
            r, g, b = color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)

        # count seconds with pixels:
        if(self.countSeconds):
            d = (self.display.width * self.display.height)
            p = ((y * self.display.width + x - self.timerFraction - 150) % d) / d
            if( p >= (1-1/d)):
                s = self.timerFraction % 1
                r = math.floor(r * (self.timerCountBrightness + (s*(1-self.timerCountBrightness))))
                g = math.floor(g * (self.timerCountBrightness + (s*(1-self.timerCountBrightness))))
                b = math.floor(b * (self.timerCountBrightness + (s*(1-self.timerCountBrightness))))
            else:
                r = math.floor(r * (self.timerCountBrightness + (p*(1-self.timerCountBrightness))))
                g = math.floor(g * (self.timerCountBrightness + (p*(1-self.timerCountBrightness))))
                b = math.floor(b * (self.timerCountBrightness + (p*(1-self.timerCountBrightness))))
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
        if(direction == "UP"):
            self.incTimer()
        elif(direction == "DOWN"):
            self.decTimer()
        elif(self.state == "set" and (direction == "LEFT" or direction == "RIGHT")):
            if(self.mode == "alarm"):
                self.mode = "off"
                self.textcolor0 = (0, 0, 0, 255)
            elif(self.mode == "off"):
                self.mode = "alarm"
                self.textcolor0 = (255, 255, 255, 255)
        self.changeRequest = True
    
    def handleConfirm(self, connection = 0):
        if(self.state == "set"):
            self.state = "run"

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
    
    def getSeparator(self):
        s = []
        for y in range(math.floor(self.size/2)):
            sx = []
            for i in range(math.floor(self.size/3)):
                if(i%3 == 1 and (y == math.floor(self.size/4)+1 or  y == math.floor(self.size/4)-1)):
                    sx.append(True)
                else:
                    sx.append(False)
            s.append(sx)
        return s
    
    def getColorsFromMessage(self, color):
        c = json.loads(color)
        return (c['r'], c['g'], c['b'], c['a'])

    def getName(self):
        return "timer"