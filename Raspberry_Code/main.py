import time, threading
from os import listdir
from os.path import isfile, join

from modes.mode import Mode
from modes.colors import Colors
from modes.menu import Menu
from modes.clock import Clock
from modes.clockanalog import ClockAnalog
from modes.text import Text
from modes.pointmoving import PointMoving
from modes.dvd import DVD
from modes.draw import Draw
from modes.video import Video
from modes.image import Image
from modes.fourrow import FourRow
from modes.snake import Snake
from modes.tetris import Tetris
from modes.life import GameOfLife
from modes.sound import Sound
from modes.fire import Fire
from modes.rain import Rain
from modes.twinkle import Twinkle
from modes.breakout import Breakout
from modes.ship import Ship
from modes.flappybird import FlappyBird
from modes.off import Off
from modes.iota import IOTA
from displays.display import Display
from connection import Connection

FRAMERATE = 60
UPDATEINTERVAL = 1/FRAMERATE

class Main:
    def __init__(self):
        self.current_mode = None
        self.setConnection()
        self.display = Display()
        # self.setMode(Colors(self, self.display))
        # self.setMode(Text(self, self.display))
        # self.setMode(Clock(self, self.display))
        # self.setMode(Menu(self, self.display))
        # self.setMode(DVD(self, self.display))
        # self.setMode(Image(self, self.display))
        # self.setMode(FourRow(self, self.display))
        # self.setMode(Snake(self, self.display))
        # self.setMode(Tetris(self, self.display))
        # self.setMode(GameOfLife(self, self.display))
        # self.setMode(Sound(self, self.display))
        # self.setMode(Breakout(self, self.display))
        # self.setMode(Fire(self, self.display))
        # self.setMode(FlappyBird(self, self.display))
        # self.setMode(Off(self, self.display))
        # self.setMode(ClockAnalog(self, self.display))
        # self.setMode(Rain(self, self.display))
        # self.setMode(Twinkle(self, self.display))
        # self.setMode(Ship(self, self.display))
        self.setMode(IOTA(self, self.display))

    def run(self):
        while(True):
            self.display.display.run_display()
            time.sleep(UPDATEINTERVAL)

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
        elif(mode == 'clockanalog'):
            modeInstance = ClockAnalog(self, self.display)
        elif(mode == 'colors'):
            modeInstance = Colors(self, self.display)
        elif(mode == 'menu'):
            modeInstance = Menu(self, self.display)
        elif(mode == 'text'):
            modeInstance = Text(self, self.display)
        elif(mode == 'pointmoving'):
            modeInstance = PointMoving(self, self.display)
        elif(mode == 'dvd'):
            modeInstance = DVD(self, self.display)
        elif(mode == 'draw'):
            modeInstance = Draw(self, self.display)
        elif(mode == 'image'):
            modeInstance = Image(self, self.display)
        elif(mode == 'video'):
            modeInstance = Video(self, self.display)
        elif(mode == 'fourrow'):
            modeInstance = FourRow(self, self.display)
        elif(mode == 'snake'):
            modeInstance = Snake(self, self.display)
        elif(mode == 'tetris'):
            modeInstance = Tetris(self, self.display)
        elif(mode == 'life'):
            modeInstance = GameOfLife(self, self.display)
        elif(mode == 'sound'):
            modeInstance = Sound(self, self.display)
        elif(mode == 'fire'):
            modeInstance = Fire(self, self.display)
        elif(mode == 'rain'):
            modeInstance = Rain(self, self.display)
        elif(mode == 'twinkle'):
            modeInstance = Twinkle(self, self.display)
        elif(mode == 'breakout'):
            modeInstance = Breakout(self, self.display)
        elif(mode == 'ship'):
            modeInstance = Ship(self, self.display)
        elif(mode == 'flappybird'):
            modeInstance = FlappyBird(self, self.display)
        elif(mode == 'off'):
            modeInstance = Off(self, self.display)
        elif(mode == 'iota'):
            modeInstance = IOTA(self, self.display)
        else:
            modeInstance = Colors(self, self.display)
        self.setMode(modeInstance)
    
    def getModes(self):
        return [f[:-3] for f in listdir("./Raspberry_Code/modes/") if isfile(join("./Raspberry_Code/modes/", f))] # print file names in modes without '.py'

main = Main()
main.run()
