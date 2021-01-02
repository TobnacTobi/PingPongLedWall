from .mode import Mode
import time

class Off(Mode):
    changeRequest = False
    
    def run(self):
        lasttime = None
        self.display.clear()
        while(not self.stop):
            time.sleep(1)

    def getName(self):
        return "off"
