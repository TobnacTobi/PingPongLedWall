import threading

class Mode(threading.Thread):
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
    
    def handleDirection(self, direction):
        pass
    
    def handleConfirm(self):
        pass

    def handleReturn(self):
        pass

    def getName(self):
        return "abstract Mode"