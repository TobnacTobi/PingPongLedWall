from .mode import Mode
import time, threading
import datetime
from displays import color_convert
from displays import texts
import math
import json
# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup

FrameRate = 20

class IOTA(Mode):
    price = "$0.00"
    brightness = 1 # between 0 and 1
    textstyle = "solid"
    textcolor0 = (255, 255, 255, 255)
    textcolor1 = (255, 255, 255, 255)
    backgroundstyle = "fadeHorizontal"
    backgroundcolor0 = (0, 0, 0, 255)
    backgroundcolor1 = (0, 0, 0, 255)
    
    def run(self):
        while(not self.stop):
            tmp = self.price
            self.price = self.getData()
            if(float(self.price[1:]) >= float(tmp[1:])):
                self.backgroundcolor0 = (0, 255, 119, 255)
                self.backgroundcolor1 = (106, 255, 0, 255)
            else:
                self.backgroundcolor0 = (255, 255, 0, 255)
                self.backgroundcolor1 = (255, 115, 0, 255)
            self.brightness = 1
            self.showPrice()

    def showPrice(self):
        maxheight = self.display.height - 2
        textarr = texts.char_to_pixels(str(self.price)+"   ", fontsize=min(maxheight, self.size*3))
        #if(len(textarr[0]) - 2 <= self.display.width): # show short texts directly without moving animation
        #    self.displayText(textarr, 0)
        #    return
        framecount = 0
        i = 0
        seconds = 0
        lasttime = None
        xpos = 0
        while(not self.changeRequest and not self.stop and seconds < 30):
            lasttime = self.wait(lasttime)
            framecount+=1
            i+=1
            if(i%FrameRate == 0):
                seconds += 1
            if(framecount > 30/self.speed):
                framecount = 0
                xpos+=1
                self.displayText(textarr, xpos)
            self.brightness = max(self.brightness - 0.02, 0.3)

    def displayText(self, textarr, xpos):
        displayWidth = self.display.width
        displayHeight = self.display.height
        maxheight = self.display.height - 2
        y0 = math.floor((self.display.height - min(maxheight, self.size*3))/2)

        for x in range(displayWidth):
            for y in range(displayHeight):
                if(y >= y0 and y - y0 < len(textarr) and textarr[y - y0][(x + xpos)%len(textarr[y - y0])]): # draw text
                    self.display.drawPixel(x, y, self.getTextColor(x, y))
                else: # draw background
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))

    def getTextColor(self, x, y):
        tr0, tg0, tb0, ta0 = self.textcolor0
        tr1, tg1, tb1, ta1 = self.textcolor1
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
        r, g, b = color_convert.MixColors((r, g, b), (0,0,0), self.brightness)
        return (r, g, b)

    def getData(self):
        # specify the url
        url = "https://coinmarketcap.com/currencies/iota/"

        # Connect to the website and return the html to the variable ‘page’
        try:
            page = urlopen(url)
        except:
            print("Error opening the IOTA URL")

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')

        # Take out the <div> of name and get its value
        div = soup.find('div', {"class": "priceValue___11gHJ"})
        print('New price retrieved: '+div.contents[0])
        return div.contents[0]

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
        return "clock"