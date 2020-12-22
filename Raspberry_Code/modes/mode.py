import threading

class Mode(threading.Thread):
    speed = 10
    size = 10
    changeRequest = False

    def __init__(self, p, d):
        super(Mode, self).__init__()
        self.parent = p
        self.display = d
        self.setDaemon(True)
        self.stop = False

    def run(self):
        pass

    def stopThread(self):
        self.stop = True
    
    def handleDirection(self, direction, connection = 0): # connection = index of connection (0, 1, 2, ..)
        pass
    
    def handleConfirm(self, connection = 0): # connection = index of connection (0, 1, 2, ..)
        pass

    def handleReturn(self):
        pass

    def handleSetting(self, settings):
        changed = False
        if(settings['speed'] != self.speed):
            self.speed = settings['speed']
            changed = True
        if(settings['size'] != self.size):
            self.size = settings['size']
            changed = True
        if(changed):
            self.changeRequest = True

    def getName(self):
        return "abstract Mode"