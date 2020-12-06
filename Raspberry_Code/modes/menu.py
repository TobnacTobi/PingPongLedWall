from .mode import Mode
import time, math, json
from displays import color_convert
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import os.path

FrameRate = 60

class Menu(Mode):
    arrowstyle = "fadeHorizontal"
    arrowcolor0 = (0, 0, 0, 150)
    arrowcolor1 = (0, 0, 0, 150)
    backgroundstyle = "rainbow"
    backgroundcolor0 = (0, 0, 0, 255)
    backgroundcolor1 = (0, 0, 0, 255)

    modeIconArray = []

    iconsize = 8 # icons in #./icons/ should have dimension of 8x8
    paddingX = 0 # calculate after arrow width is clear
    paddingY = 0 # calculate in run method
    destinationIndex = 0
    destinationX = 0 # position of the selected mode (destinationIndex*(iconsize+padding)) <=> the position i want to animate to
    currentX = 0 # position of the current display -> change with calculated speed to match destinationX

    def run(self):
        self.modes = self.parent.getModes()
        self.modes.remove('mode')
        self.modes.remove('menu')

        self.arrows = self.getArrowArrays()
        self.paddingX = math.floor((self.display.width - len(self.arrows[0][0])*2 - self.iconsize)/2)
        self.paddingY = math.floor((self.display.height - self.iconsize)/2)

        self.modeIconArray = self.getPaddingArray()
        for mode in self.modes:
            filename = './Raspberry_Code/modes/icons/'+mode+'.icon.png'
            if (not os.path.isfile(filename)):
                filename = './Raspberry_Code/modes/icons/default.icon.png'
            img = Image.open(filename) # https://stackoverflow.com/questions/25102461/python-rgb-matrix-of-an-image
            arr = np.array(img) # list of rows -> list of columns -> list of values that represent rgb color | arr[row][column][rgba in [0,3]]
            self.modeIconArray = np.concatenate((self.modeIconArray, arr), axis=1)
            if(not mode == self.modes[-1]):
                self.modeIconArray = np.concatenate((self.modeIconArray, self.getPaddingArray()), axis=1)

        self.display.clear()
        while(not self.stop):
            self.draw()
            self.animate()
            time.sleep(1/FrameRate)

    def animate(self):
        if(self.currentX == self.destinationX):
            return
        if(abs(self.destinationX - self.currentX) < 0.5):
            self.currentX = self.destinationX
            return
        self.currentX += max(math.floor((self.destinationX - self.currentX)*2*self.speed/FrameRate), 1, key=abs)

    def draw(self):
        leftarrow, rightarrow = self.arrows
        leftY0 = math.floor((self.display.height - len(leftarrow))/2)
        rightY0 = math.floor((self.display.height - len(rightarrow))/2)
        rightX0 = math.floor((self.display.width) - len(rightarrow[0]))
        for x in range(self.display.width):
            for y in range(self.display.height):
                if( y >= self.paddingY and y - self.paddingY < len(self.modeIconArray)):
                    if(y >= leftY0 and y - leftY0 < len(leftarrow) and x < len(leftarrow[y-leftY0]) and leftarrow[y-leftY0][x] or
                        y >= rightY0 and y - rightY0 < len(rightarrow) and x>= rightX0 and x - rightX0 < len(rightarrow[y-leftY0]) and rightarrow[y-leftY0][x - rightX0]):
                        self.display.drawPixel(x, y, self.getArrowColor(x, y, True))
                    else:
                        self.display.drawPixel(x, y, self.getIconColor(self.modeIconArray[y-self.paddingY][(x + self.currentX) % len(self.modeIconArray[0])], x, y))
                    continue

                if(y >= leftY0 and y - leftY0 < len(leftarrow) and x < len(leftarrow[y-leftY0]) and leftarrow[y-leftY0][x]): # draw left arrow
                    self.display.drawPixel(x, y, self.getArrowColor(x, y))
                    continue
                elif(y >= rightY0 and y - rightY0 < len(rightarrow) and
                     x>= rightX0 and x - rightX0 < len(rightarrow[y-leftY0]) and rightarrow[y-leftY0][x - rightX0]): # draw right arrow
                    self.display.drawPixel(x, y, self.getArrowColor(x, y))
                    continue
                #currentXIconOffset = (self.currentX % (self.iconsize + self.paddingX)) + self.paddingX + len(leftarrow[0])
                #currentModeIndex = math.floor(((self.currentX-currentXIconOffset-x) / (self.iconsize + self.paddingX)) % len(self.modes))
                #
                #if( y >= self.paddingY and y - self.paddingY < len(self.modeArrays[currentModeIndex]) and 
                #    x >= currentXIconOffset and x - currentXIconOffset < len(self.modeArrays[currentModeIndex][y-self.paddingY])): # draw icon in position self.currentX
                #    self.display.drawPixel(x, y, self.getIconColor(self.modeArrays[currentModeIndex][y-self.paddingY][x-currentXIconOffset], x, y))
                else: # draw background
                    self.display.drawPixel(x, y, self.getBackgroundColor(x, y))

    def getArrowArrays(self):
        height = math.floor(self.display.height*2/3)
        width = math.floor(self.display.width/5)
        s1 = []
        s2 = []
        for y in range(height):
            sx1 = []
            sx2 = []
            for x in range(width):
                if(x/width >= abs(y - height/2)/(height/2)):
                    sx1.append(True)
                else:
                    sx1.append(False)
            s1.append(sx1)
            s2.append(sx1[::-1])
        return (s1, s2)
    
    def getPaddingArray(self):
        s = []
        color = [0,0,0,0]
        for y in range(self.iconsize):
            sx = []
            for x in range(self.paddingX + len(self.arrows[0][0])):
                sx.append(color)
            s.append(sx)
        return s
    
    def getIconColor(self, rgba, x, y):
        r = rgba[0]
        g = rgba[1]
        b = rgba[2]
        a = rgba[3]
        if(a == 255):
            return (r, g, b)
        br, bg, bb = self.getBackgroundColor(x, y)
        r = math.floor(a*(r)/255 + (br)*(255-a)/255)
        g = math.floor(a*(g)/255 + (bg)*(255-a)/255)
        b = math.floor(a*(b)/255 + (bb)*(255-a)/255)
        return (r, g, b)

    def getArrowColor(self, x, y, over_text = False, opacity = 1.0):
        tr0, tg0, tb0, ta0 = self.arrowcolor0
        tr1, tg1, tb1, ta1 = self.arrowcolor1
        if(not opacity == 1.0):
            ta0*=opacity
            ta1*=opacity
        br = bg = bb = 0
        if(over_text):
            br, bg, bb = self.getIconColor(self.modeIconArray[y-self.paddingY][(x + self.currentX) % len(self.modeIconArray[0])], x, y)
        else:
            br, bg, bb = self.getBackgroundColor(x, y)
        if(self.arrowstyle == 'solid'):
            if(ta0 == 255):
                return (tr0, tg0, tb0)
            r = math.floor(ta0*(tr0)/255 + (br)*(255-ta0)/255)
            g = math.floor(ta0*(tg0)/255 + (bg)*(255-ta0)/255)
            b = math.floor(ta0*(tb0)/255 + (bb)*(255-ta0)/255)
            return (r, g, b)
        if(self.arrowstyle == 'fadeHorizontal'):
            length = self.display.width
            p = (x %length)/length
            r = math.floor((p)*(tr0) + (tr1)*(1-p))
            g = math.floor((p)*(tg0) + (tg1)*(1-p))
            b = math.floor((p)*(tb0) + (tb1)*(1-p))
            a = math.floor((p)*(ta0) + ta1*(1-p))

            r = math.floor(a*(r)/255 + (br)*(255-a)/255)
            g = math.floor(a*(g)/255 + (bg)*(255-a)/255)
            b = math.floor(a*(b)/255 + (bb)*(255-a)/255)

            return (r, g, b)
        if(self.arrowstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            r = math.floor((p)*(tr0) + (tr1)*(1-p))
            g = math.floor((p)*(tg0) + (tg1)*(1-p))
            b = math.floor((p)*(tb0) + (tb1)*(1-p))
            a = math.floor((p)*(ta0) + ta1*(1-p))

            r = math.floor(a*(r)/255 + (br)*(255-a)/255)
            g = math.floor(a*(g)/255 + (bg)*(255-a)/255)
            b = math.floor(a*(b)/255 + (bb)*(255-a)/255)

            return (r, g, b)
        if(self.arrowstyle == 'rainbow'):
            xpos = time.time()*0.05%1
            size = 30/self.size
            return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)
    
    def getBackgroundColor(self, x, y):
        br0, bg0, bb0, ba0 = self.backgroundcolor0
        br1, bg1, bb1, ba1 = self.backgroundcolor1
        if(self.backgroundstyle == 'solid'):
            if(ba0 == 255):
                return (br0, bg0, bb0)
            return (br0 * (ba0 / 255), bg0* (ba0 / 255), bb0* (ba0 / 255))
        if(self.backgroundstyle == 'fadeHorizontal'):
            length = self.display.width
            p = (x%length)/length
            r = math.floor((p)*(br0) + (br1)*(1-p))
            g = math.floor((p)*(bg0) + (bg1)*(1-p))
            b = math.floor((p)*(bb0) + (bb1)*(1-p))
            return (r, g, b)
        if(self.backgroundstyle == 'fadeVertical'):
            length = self.display.height
            p = (y%length)/length
            r = math.floor((p)*(br0) + (br1)*(1-p))
            g = math.floor((p)*(bg0) + (bg1)*(1-p))
            b = math.floor((p)*(bb0) + (bb1)*(1-p))
            return (r, g, b)
        if(self.backgroundstyle == 'rainbow'):
            xpos = time.time()*0.01%1
            size = 5/self.size
            return color_convert.HSVtoRGB((xpos + size*(x+y)/(self.display.width+self.display.height)/2) % 1.0, 1, 1)

    def handleModeSetting(self, t):
        tc = json.loads(t['arrowcolor'])
        self.arrowstyle = tc['style']
        print(self.arrowstyle)
        self.arrowcolor0 = self.getColorsFromMessage(tc['color0'])
        if(tc['style'] == 'fadeHorizontal' or tc['style'] == 'fadeVertical'):
            self.arrowcolor1 = self.getColorsFromMessage(tc['color1'])
        bc = json.loads(t['backgroundcolor'])
        self.backgroundstyle = bc['style']
        self.backgroundcolor0 = self.getColorsFromMessage(bc['color0'])
        if(bc['style'] == 'fadeHorizontal' or bc['style'] == 'fadeVertical'):
            self.backgroundcolor1 = self.getColorsFromMessage(bc['color1'])
        self.changeRequest = True

    def handleDirection(self, direction):
        if(direction == "RIGHT"):
            self.destinationIndex += 1
            self.destinationX += (self.paddingX + len(self.arrows[0][0]) + self.iconsize)
        elif(direction == "LEFT"):
            self.destinationIndex -= 1
            self.destinationX -= (self.paddingX + len(self.arrows[0][0]) + self.iconsize)
        
        self.changeRequest = True
    
    def handleConfirm(self):
        self.parent.setModeByName(self.modes[self.destinationIndex % len(self.modes)])
    
    def getName(self):
        return "menu"