from .mode import Mode
import time
from displays import color_convert
from random import random
import math
from opensimplex import OpenSimplex

changeAfterSeconds = 30
FrameRate = 60

class Colors(Mode):
    speed = 10
    size = 10
    changeRequest = False
    
    def run(self):
        while(not self.stop):
            self.spiral()
            self.diagonal_rainbow()
            self.rainbow_angle()
            self.rainbow_rotate()
            self.noise()
            self.random_colors()
    
    def spiral(self):
        start_color_hue_angle = 0.0
        timepast = 0
        width = self.display.width
        height = self.display.height
        maxdistance = math.sqrt((width/2)*(width/2) + (height/2)*(height/2))
        angle = 0
        speed = self.speed*0.0002
        size = self.size/20
        lasttime = self.wait()
        while(not self.changeAnimation(timepast)):
            for x in range(width):
                for y in range(height):
                    distance = math.sqrt((x-width/2)*(x-width/2) + (y-height/2)*(y-height/2))
                    self.display.drawPixel(x, y, color_convert.HSVtoRGB(-start_color_hue_angle+size*distance/maxdistance+math.atan2(y-(height/2), x-(width/2))/(2*math.pi) % 1.0, 1, 1))
            start_color_hue_angle+=speed
            angle = (angle + 0.05) % (math.pi*2)
            if(start_color_hue_angle>1):
                start_color_hue_angle = 0
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate

    def rainbow_rotate(self):
        start_color_hue_angle = 0.0
        timepast = 0
        width = self.display.width
        height = self.display.height
        angle = 0
        speed = self.speed*0.0002
        lasttime = self.wait()
        while(not self.changeAnimation(timepast)):
            for x in range(width):
                for y in range(height):
                    self.display.drawPixel(x, y, color_convert.HSVtoRGB(start_color_hue_angle+math.atan2(y-(height/2), x-(width/2))/(2*math.pi) % 1.0, 1, 1))
            start_color_hue_angle+=speed
            angle = (angle + 0.05) % (math.pi*2)
            if(start_color_hue_angle>1):
                start_color_hue_angle = 0
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate

    def rainbow_angle(self):
        start_color_hue_angle = 0.0
        timepast = 0
        width = self.display.width
        height = self.display.height
        angle = 0
        speed = self.speed*0.0001
        size = 10/self.size
        lasttime = self.wait()
        while(not self.changeAnimation(timepast)):
            for x in range(width):
                for y in range(height):
                    self.display.drawPixel(x, y, color_convert.HSVtoRGB((start_color_hue_angle + (math.sin(angle) * size*(height/2-y) + math.cos(angle) * size*(width/2-x))/(width+height)) % 1.0, 1, 1))
            start_color_hue_angle+=speed
            angle = (angle + speed*10) % (math.pi*2)
            if(start_color_hue_angle>1):
                start_color_hue_angle = 0
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate

    def random_colors(self):
        timepast = 0
        width = self.display.width
        height = self.display.height
        lasttime = self.wait()
        while(not self.changeAnimation(timepast)):
            for i in range(width*height):
                self.display.drawPixel(math.floor(random()*width), math.floor(random()*height), color_convert.HSVtoRGB(random(), 1, 1))
                lasttime = self.wait(lasttime)
                timepast += (1/FrameRate)
                if(timepast > changeAfterSeconds):
                    break

    def diagonal_rainbow(self):
        start_color_hue_angle = 0.0
        timepast = 0
        width = self.display.width
        height = self.display.height
        speed = self.speed*0.0001
        size = 10/self.size
        lasttime = self.wait()
        while(not self.changeAnimation(timepast)):
            for x in range(width):
                for y in range(height):
                    self.display.drawPixel(x, y, color_convert.HSVtoRGB((start_color_hue_angle + size*(x+y)/(width+height)/2) % 1.0, 1, 1))
            start_color_hue_angle+=speed
            if(start_color_hue_angle>1):
                start_color_hue_angle = 0
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate
    
    def noise(self):
        timepast = 0
        posx = 0
        posy = 0
        zoom = 0
        movement = OpenSimplex(math.floor(random()*1000))
        tmp = OpenSimplex(math.floor(random()*1000))
        speed = self.speed*0.01
        i = 0
        lasttime = self.wait()
        while(not self.changeAnimation(timepast)):
            posx += movement.noise2d(0, i/100)*speed
            posy += movement.noise2d(10, i/100)*speed
            zoom = (movement.noise2d(50, i/100) + 1.1) * 1.3
            i += 1
            for x in range(self.display.width):
                for y in range(self.display.height):
                    output = ((tmp.noise2d((x*zoom+ posx)/10, (y*zoom + posy)/10) + 1) / 2) ** 2
                    self.display.drawPixel(x, y, color_convert.HSVtoRGB(output, 1, 1))
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate
    
    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime
    
    def changeAnimation(self, timepast):
        v = (timepast > changeAfterSeconds or self.stop or self.changeRequest)
        self.changeRequest = False
        return v

    def handleDirection(self, direction):
        self.changeRequest = True
    
    def handleConfirm(self):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True

    def getName(self):
        return "colors"