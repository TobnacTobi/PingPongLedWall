from .mode import Mode
import time
from displays import color_convert
from displays import texts
import math
import json

FrameRate = 60

class Text(Mode):
    xpos = 0 # defines the start position of the text (how far in the text have we come?)
    text = "Text"
    textarr = []
    speed = 20
    textstyle = "solid"
    textcolor0 = (255, 255, 255, 255)
    textcolor1 = (255, 255, 255, 255)
    backgroundstyle = "solid"
    backgroundcolor0 = (0, 0, 0, 255)
    backgroundcolor1 = (0, 0, 0, 255)
    
    def run(self):
        while(not self.stop):
            self.display.clear()
            self.xpos = 0
            self.textarr = self.getTextMatrix()
            if(len(self.textarr[0]) - 2 <= self.display.width): # show short texts directly without moving animation
                self.displayText()
                while(not self.changeRequest and not self.stop):
                    self.wait()
            else:
                self.animateText()
            self.changeRequest = False


    def animateText(self):
        framecount = 0
        lasttime = None
        while(not self.changeRequest and not self.stop):
            lasttime = self.wait(lasttime)
            framecount+=1
            if(framecount > 100/self.speed):
                framecount = 0
                self.xpos+=1
                self.displayText()

    def displayText(self):
        displayWidth = self.display.width
        displayHeight = self.display.height
        maxheight = self.display.height - 2
        y0 = math.floor((self.display.height - min(maxheight, self.size))/2)+2
        #self.display.clear()
        for x in range(displayWidth):
            for y in range(displayHeight):
                if(y >= y0 and y - y0 < len(self.textarr) and self.textarr[y - y0][(x + self.xpos)%len(self.textarr[y - y0])]): # draw text
                    self.display.drawPixel(x, y, self.getTextColor(x, y, y0))
                else: # draw background
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))

    def getTextMatrix(self):
        maxheight = self.display.height - 2
        return texts.char_to_pixels(self.text, fontsize=min(maxheight, self.size))

    def getTextColor(self, x, y, y0):
        tr0, tg0, tb0, ta0 = self.textcolor0
        tr1, tg1, tb1, ta1 = self.textcolor1
        br, bg, bb = self.getBackgroundColor(x, y)
        if(self.textstyle == 'solid'):
            if(ta0 == 255):
                return (tr0, tg0, tb0)
            r = math.floor(ta0*(tr0)/255 + (br)*(255-ta0)/255)
            g = math.floor(ta0*(tg0)/255 + (bg)*(255-ta0)/255)
            b = math.floor(ta0*(tb0)/255 + (bb)*(255-ta0)/255)
            return (r, g, b)
        if(self.textstyle == 'fadeHorizontal'):
            length = len(self.textarr[y - y0])
            p = ((x + self.xpos)%length)/length
            r = math.floor((p)*(tr0) + (tr1)*(1-p))
            g = math.floor((p)*(tg0) + (tg1)*(1-p))
            b = math.floor((p)*(tb0) + (tb1)*(1-p))
            a = math.floor((p)*(ta0) + ta1*(1-p))

            r = math.floor(a*(r)/255 + (br)*(255-a)/255)
            g = math.floor(a*(g)/255 + (bg)*(255-a)/255)
            b = math.floor(a*(b)/255 + (bb)*(255-a)/255)

            return (r, g, b)
        if(self.textstyle == 'fadeVertical'):
            length = len(self.textarr)
            p = ((y - y0)%length)/length
            r = math.floor((p)*(tr0) + (tr1)*(1-p))
            g = math.floor((p)*(tg0) + (tg1)*(1-p))
            b = math.floor((p)*(tb0) + (tb1)*(1-p))
            a = math.floor((p)*(ta0) + ta1*(1-p))

            r = math.floor(a*(r)/255 + (br)*(255-a)/255)
            g = math.floor(a*(g)/255 + (bg)*(255-a)/255)
            b = math.floor(a*(b)/255 + (bb)*(255-a)/255)

            return (r, g, b)
        if(self.textstyle == 'rainbow'):
            xpos = self.xpos*0.01%1
            size = 30/self.size
            return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)

    def getBackgroundColor(self, x, y):
        
        if(self.backgroundstyle == 'solid'):
            br0, bg0, bb0, ba0 = self.backgroundcolor0
            if(ba0 == 255):
                return (br0, bg0, bb0)
            return (br0 * (ba0 / 255), bg0* (ba0 / 255), bb0* (ba0 / 255))
        if(self.backgroundstyle == 'fadeHorizontal'):
            length = self.display.width
            p = (x%length)/length
            return color_convert.MixColors(self.backgroundcolor0[:-1], self.backgroundcolor1[:-1], p)
        if(self.backgroundstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            return color_convert.MixColors(self.backgroundcolor0[:-1], self.backgroundcolor1[:-1], p)
        if(self.backgroundstyle == 'rainbow'):
            xpos = self.xpos*0.005%1
            size = 10/self.size
            return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)

    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime
    
    def handleDirection(self, direction):
        self.changeRequest = True
    
    def handleConfirm(self):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True

    def handleModeSetting(self, t):
        if(t['text'] == '' or t['text'] is None):
            return
        self.text = t['text']
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
        return "text"