from .mode import Mode
import time

class Clock(Mode):
    def run(self):
        color = (0,0,0xFF)
        x = 0
        y = 0
        while(not self.stop):
            self.display.drawPixel(x, y, color)
            x+=1
            if(x >= self.display.width):
                x = 0
                y += 1
            if(y >= self.display.height):
                y = 0
            color = (0,0,0xFF)
            time.sleep(0.0333)
    
    def getName(self):
        return "clock"
    