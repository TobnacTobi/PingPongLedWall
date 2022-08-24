from .mode import Mode
import time
from displays import color_convert
from random import random
import math
from opensimplex import OpenSimplex
from PIL import Image
import numpy as np

FrameRate = 60

class Colors(Mode):
    changeAnimationRequest = False

    def run(self):
        while(not self.stop):
            self.circle()
            self.waves()
            self.spiral()
            self.diagonal_rainbow()
            self.rainbow_angle()
            self.rainbow_rotate()
            self.noise()
            self.random_colors()
            self.mandelbrot()
            
    def getMandelbrot(self, zoom): # zoom value in (0, 1]
        # drawing area 
        #point = (-math.e/7, -math.e/20)
        #point = (-0.761574,-0.0847596)
        point = (-0.7746806106269039, -0.1374168856037867)
        xa = point[0] - zoom
        xb = point[0] + zoom
        ya = point[1] - zoom
        yb = point[1] + zoom

        # max iterations allowed 
        maxIt = 255 

        # image size 
        imgx = self.display.width
        imgy = self.display.height
        image = Image.new("RGB", (imgx, imgy)) 

        for y in range(imgy): 
            zy = y * (yb - ya) / (imgy - 1)  + ya 
            for x in range(imgx): 
                zx = x * (xb - xa) / (imgx - 1)  + xa 
                z = zx + zy * 1j
                c = z 
                for i in range(maxIt): 
                    if abs(z) > 2.0: break
                    z = z * z + c 
                image.putpixel((x, y), ((30 * i) % 256, (4 * i) % 256, (255 - (30 * i)) % 256))
                #image.putpixel((x, y), (i % 4 * 64, i % 8 * 32, i % 16 * 16)) 
        arr = np.asarray(image)
        return arr

    def mandelbrot(self):
        timepast = 0
        lasttime = self.wait()
        zoom = 2
        while(not self.changeAnimation(timepast)):
            arr = self.getMandelbrot(zoom)
            for y in range(self.display.height):
                for x in range(self.display.width):
                    self.display.drawPixel(x, y, arr[y][x])
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate
            zoom = zoom*(0.99**(10/self.speed))



    def waves(self):
        timepast = 0
        start_color_hue_angle = 0.0
        width = self.display.width
        height = self.display.height
        angle = 0
        speed = self.speed*0.0001
        size = 10/self.size
        lasttime = self.wait()
        
        while(not self.changeAnimation(timepast)):
            if(self.changeRequest):
                speed = self.speed*0.0001
                size = 10/self.size
                self.changeRequest = False
            for x in range(width):
                for y in range(height):
                    self.display.drawPixel(x, y, 
                        color_convert.HSVtoRGB(
                            (start_color_hue_angle + (math.sin(angle) * size*(height/2-y) + math.cos(angle) * size*(width/2-x))/(width+height)) % 1.0,
                            1, 
                            -(start_color_hue_angle*self.speed+ (math.sin(angle)*size*(height/2-y) + math.cos(angle)*size*(width/2-x))/(math.sin(angle)*height + math.cos(angle)*width)) % 0.8 + 0.2
                        )
                    )
            start_color_hue_angle+=speed
            angle = (angle + speed) % (math.pi*2)
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate

    def circle(self):
        start_color_hue_angle = 0.0
        timepast = 0
        width = self.display.width
        height = self.display.height
        maxdistance = math.sqrt((width/2)*(width/2) + (height/2)*(height/2))
        posx = width/2
        posy = height/2
        movement = OpenSimplex(math.floor(random()*1000))
        angle = 0
        speed = self.speed*0.0002
        size = 5/self.size
        lasttime = self.wait()
        i = 0
        while(not self.changeAnimation(timepast)):
            if(self.changeRequest):
                speed = self.speed*0.0002
                size = 5/self.size
                self.changeRequest = False
            posx = max(0, min(posx + (movement.noise2(0, i/500))*speed, self.display.width))
            posy = max(0, min(posy + (movement.noise2(300, i/500))*speed, self.display.height))
            for x in range(width):
                for y in range(height):
                    distance = math.sqrt((x-posx)*(x-posx) + (y-posy)*(y-posy))
                    self.display.drawPixel(x, y, 
                        color_convert.HSVtoRGB(
                            -start_color_hue_angle+size*distance/maxdistance % 1.0,
                            1, 1))
            start_color_hue_angle+=speed
            angle = (angle + 0.05) % (math.pi*2)
            if(start_color_hue_angle>1):
                start_color_hue_angle = 0
            lasttime = self.wait(lasttime)
            timepast += 1/FrameRate
            i+=1
    
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
            if(self.changeRequest):
                speed = self.speed*0.0002
                size = self.size/20
                self.changeRequest = False
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
            if(self.changeRequest):
                angle = 0
                speed = self.speed*0.0002
                self.changeRequest = False
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
        movement = OpenSimplex(math.floor(random()*1000)) # for noise brightness
        tmp = OpenSimplex(math.floor(random()*1000)) # for noise brightness
        i=0 # for noise brightness
        posx = posy = 0 # for noise brightness

        
        start_color_hue_angle = 0.0
        timepast = 0
        width = self.display.width
        height = self.display.height
        angle = 0
        speed = self.speed*0.0001
        size = 10/self.size
        lasttime = self.wait()
        while(not self.changeAnimation(timepast)):
            if(self.changeRequest):
                speed = self.speed*0.0001
                size = 10/self.size
                self.changeRequest = False

            posx += (movement.noise2(0, i/500))*self.speed*0.01   # for noise brightness
            posy += (movement.noise2(300, i/500))*self.speed*0.01 # for noise brightness
            zoom = (movement.noise2(1000, i/300) + 1.1) * 1.3     # for noise brightness
            i+=1                                                   # for noise brightness
            
            for x in range(width):
                for y in range(height):
                    output = ((tmp.noise2(((x-self.display.width)*zoom + posx)/10, ((y-self.display.height)*zoom + posy)/10) + 1) / 2) ** 2 # noise brightness
                    self.display.drawPixel(x, y, color_convert.HSVtoRGB((start_color_hue_angle + (math.sin(angle) * size*(height/2-y) + math.cos(angle) * size*(width/2-x))/(width+height)) % 1.0, 1, 0.1 + 0.9*output))
                    # self.display.drawPixel(x, y, color_convert.HSVtoRGB((start_color_hue_angle + (math.sin(angle) * size*(height/2-y) + math.cos(angle) * size*(width/2-x))/(width+height)) % 1.0, 1, 1))
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
        self.display.clear()
        lasttime = self.wait()
        stop = False
        while(not self.changeAnimation(timepast) and not stop):
            if(self.changeRequest):
                speed = self.speed*0.0001
                size = 10/self.size
                self.changeRequest = False
            for i in range(width*height):
                self.display.drawPixel(math.floor(random()*width), math.floor(random()*height), color_convert.HSVtoRGB(random(), random(), random()))
                if(i % self.speed == 0):
                    lasttime = self.wait(lasttime)
                timepast += (1/FrameRate)
                if(self.changeAnimation(timepast)):
                    stop = True
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
            if(self.changeRequest):
                speed = self.speed*0.0001
                size = 10/self.size
                self.changeRequest = False
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
            if(self.changeRequest):
                speed = self.speed*0.01
                self.changeRequest = False
            posx += (movement.noise2(0, i/500))*speed
            posy += (movement.noise2(300, i/500))*speed
            zoom = (movement.noise2(1000, i/300) + 1.1) * 1.3
            i += 1
            for x in range(self.display.width):
                for y in range(self.display.height):
                    output = ((tmp.noise2(((x-self.display.width)*zoom + posx)/10, ((y-self.display.height)*zoom + posy)/10) + 1) / 2) ** 2
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
        #v = (timepast > changeAfterSeconds or self.stop or self.changeRequest)
        v = (self.changeAnimationRequest or self.stop)
        self.changeAnimationRequest = False
        return v

    def handleDirection(self, direction, connection = 0):
        self.changeAnimationRequest = True
    
    def handleConfirm(self, connection = 0):
        self.changeAnimationRequest = True

    def handleReturn(self):
        self.changeAnimationRequest = True

    def getName(self):
        return "colors"
