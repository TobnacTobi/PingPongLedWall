from .mode import Mode
import time
from displays import color_convert
import math
from io import BytesIO
import base64
from PIL import Image as im
import numpy as np

changeAfterSeconds = 30
FrameRate = 60

class Video(Mode):
    changeRequest = True
    image = None

    def run(self):
        lasttime = self.wait()
        while(not self.stop):
            if(self.changeRequest):
                self.draw()
                self.changeRequest = False
            lasttime = self.wait(lasttime)

    def draw(self):
        if(self.image is None):
            return

        self.image.thumbnail((self.display.width, self.display.height))
        arr = np.array(self.image)
        for y in range(self.display.height):
            for x in range(self.display.width):
                self.display.drawPixel(x, y, arr[y][x])

    def wait(self, lasttime=None):
        if(lasttime is None):
            time.sleep(1/FrameRate)
            return time.time()
        currtime = time.time()
        if(currtime - 1/FrameRate < lasttime):
            time.sleep(1/FrameRate-(currtime - lasttime))
            return time.time()
        return currtime

    def handleModeSetting(self, t):
        print(t)
        if('image' in t):
            self.image = im.open(BytesIO(base64.b64decode(t['image'])))
        print('decoded')
        self.changeRequest = True

    def handleDirection(self, direction, connection = 0):
        self.changeRequest = True
    
    def handleConfirm(self, connection = 0):
        self.changeRequest = True

    def handleReturn(self):
        self.changeRequest = True

    def getName(self):
        return "video"