import time, threading
from os import listdir
from os.path import isfile, join

from modes.mode import Mode
from modes.colors import Colors
from modes.menu import Menu
from modes.clock import Clock
from modes.text import Text
from modes.pointmoving import PointMoving
from displays.display import Display
from connection import Connection

class Main:
    def __init__(self):
        self.current_mode = None
        self.setConnection()
        self.display = Display()
        # self.setMode(Colors(self, self.display))
        # self.setMode(Text(self, self.display))
        # self.setMode(Clock(self, self.display))
        self.setMode(Menu(self, self.display))

    def run(self):
        while(True):
            self.display.display.run_display()
            time.sleep(0.016)
            # only necessary for the pygame display

    def setConnection(self):
        self.connection = Connection(self)
        self.connection.start()
    
    def setMode(self, mode: Mode):
        if(self.current_mode is not None  and  issubclass(self.current_mode.__class__, threading.Thread) and issubclass(self.current_mode.__class__, Mode)):
            self.current_mode.stopThread()
        if(not (issubclass(mode.__class__, threading.Thread) or issubclass(mode.__class__, Mode))):
            raise Exception('Given mode Class does not inherit Mode or Thread. sad :(')
        self.current_mode = mode
        self.current_mode.start()
        message = {}
        message['type'] = 'MODE'
        message['data'] = self.current_mode.getName()
        message['comment'] = 'Selected mode'
        self.connection.sendMessage(message)
    
    def setModeByName(self, mode: str):
        modeInstance = None
        if(mode == 'clock'):
            modeInstance = Clock(self, self.display)
        elif(mode == 'colors'):
            modeInstance = Colors(self, self.display)
        elif(mode == 'menu'):
            modeInstance = Menu(self, self.display)
        elif(mode == 'text'):
            modeInstance = Text(self, self.display)
        elif(mode == 'pointmoving'):
            modeInstance = PointMoving(self, self.display)
        else:
            modeInstance = Colors(self, self.display)
        self.setMode(modeInstance)
    
    def getModes(self):
        return [f[:-3] for f in listdir("./Raspberry_Code/modes/") if isfile(join("./Raspberry_Code/modes/", f))] # print file names in modes without '.py'

main = Main()
main.run()