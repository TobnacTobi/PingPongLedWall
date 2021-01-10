from .mode import Mode
import time
from displays import color_convert
import math
from io import BytesIO
import base64
import socket
import threading
import struct
from PIL import Image as im
import numpy as np

changeAfterSeconds = 30
FrameRate = 60

class Video(Mode):
    changeRequest = True
    image = None

    def run(self):
        lasttime = self.wait()
        print("[STARTING] VIDEO SOCKET is starting")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8943))
        print("[OPEN] VIDEO SOCKET is accessible under: " + str(server_socket.getsockname()))
        server_socket.listen(1)
        while(not self.stop):
            (client_socket, addr) = server_socket.accept()
            thread = threading.Thread(target=self.handleClient, args=(client_socket, addr))
            thread.start()
        server_socket.close()
        #while(not self.stop):
        #    if(self.changeRequest):
        #        self.draw()
        #        self.changeRequest = False
        #    lasttime = self.wait(lasttime)
    
    def handleClient(self, conn, addr):
        print(f"[NEW VIDEO] from: {addr}")
        connected = True
        while connected:
            try:
                data = b''
                data += conn.recv(2048)
                self.handleImage(data)
            except ConnectionResetError as e:
                connected = False
                print('Connection Error on VIDEO SOCKET')

        conn.close()

    def handleImage(self, img):
        try:
            self.image = im.open(BytesIO(img))
            self.draw(self.image)
        except Exception as e:
            print('invalid image caught')
            print(e)

    def draw(self, image):
        if(image is None):
            return

        arr = np.array(image)
        try:
            for y in range(self.display.height):
                for x in range(self.display.width):
                    self.display.drawPixel(x, y, arr[y][x])
        except Exception as e:
            print('COULD NOT DRAW IMAGE')
            print(e)
            print(image)
            print(arr)

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