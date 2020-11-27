from .mode import Mode
import time

class Menu(Mode):
    def run(self):
        color = (0xFF,0,00)
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
            color = (0xFF,0,00)
            time.sleep(0.0333)
    
    def getName(self):
        return "menu"