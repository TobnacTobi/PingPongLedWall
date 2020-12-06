import time

class Display:
    width = 20
    height = 15
    def __init__(self):
        from .pygame_display import PYGameDisplay
        self.display = PYGameDisplay(self.width, self.height)
        #from .led_display import LEDDisplay
        #self.display = LEDDisplay(20, 15)

    def drawPixel(self, x, y, color):
        self.display.drawPixel(x, y, color)
    
    def setBrightness(self, b):
        ## instant:
        self.display.setBrightness(b)

        ## with animation/blending:
        #currentBrightness = self.display.brightness
        #steps = 10
        #brightnessStep = (b - currentBrightness)/steps
        #for step in range(steps):
        #    currentBrightness += brightnessStep
        #    self.display.setBrightness(currentBrightness)
        #    time.sleep(0.1)
    #
    def drawRow(self, y, color):
        for x in range(self.width):
            self.display.drawPixel(x, y, color)
    
    def drawColumn(self, x, color):
        for y in range(self.height):
            self.display.drawPixel(x, y, color)
    
    def clear(self):
        for x in range (self.width):
            for y in range(self.height):
                self.display.drawPixel(x, y, (0,0,0))







class DisplayInterface:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.brightness = 100 # 0 to 100
        display = [[0 for x in range(self.width)] for y in range(self.height)]

    def drawPixel(self):
        pass

    def setBrightness(self, b):
        """
        b in [0, 100]
        gets multiplied with actual brightness of the pixel (dark pixels stay dark)
        """
        self.brightness = b