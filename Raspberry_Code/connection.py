import time, threading
import json
import socket
import sys
#tuya control:
import configparser
from tuyalinksdk.client import TuyaClient
from tuyalinksdk.console_qrcode import qrcode_generate

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = '{"type":"DISCONNECT"'
SEPARATOR = "|"

class Connection(threading.Thread):
    client_sockets = []
    
    def __init__(self, p):
        super(Connection, self).__init__()
        self.parent = p
        self.setDaemon(True)
        self.message = {"type": "WELCOME", "data": "", "comment": ""}
        
    def run(self):
        print("[STARTING] Server is starting")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 8942))
        print("[OPEN] Server is accessible under: " + str(server_socket.getsockname()))
        server_socket.listen(2)
        
        #initialize tuya service:
        config = configparser.ConfigParser()
        config.read('config')
        
        tuyaconfig = config['tuya']
        pid = tuyaconfig['productid']
        uuid = tuyaconfig['uuid']
        ak = tuyaconfig['authkey']
        
        self.tuyaClient = TuyaClient(productid=pid, uuid=uuid, authkey=ak)
        self.tuyaClient.on_connected = self.onConnected
        self.tuyaClient.on_qrcode = self.onQRCode
        self.tuyaClient.on_reset = self.onReset
        self.tuyaClient.on_dps = self.onDataPointSet
        self.tuyaClient.connect()
        self.tuyaClient.loop_start()
        self.tuyaClient.push_dps({'101': True})

        #runloop:
        while(True):
            (client_socket, addr) = server_socket.accept()
            thread = threading.Thread(target=self.handleClient, args=(client_socket, addr))
            thread.start()

    def handleClient(self, conn, addr):
        self.client_sockets.append(conn)
        print(f"[NEW CONNECTION] from: {addr} | Total Connections: {len(self.client_sockets)}")
        connected = True
        while connected:
            #msg_length = conn.recv(HEADER)
            #if msg_length:
            #    print(msg_length)
            #    msg_length = int.from_bytes(msg_length, byteorder='little', signed=False)
            #    msg_length = int(msg_length)
            #    print(msg_length)
            msg = ""
            try:
                while(True and conn in self.client_sockets):
                    msg += conn.recv(1024).decode(FORMAT)
                    pieces = msg.split(SEPARATOR)
                    msg = pieces.pop()
                    for piece in pieces:
                        if(piece.startswith(DISCONNECT_MESSAGE) or not piece):
                            connected = False
                            self.client_sockets.remove(conn)
                            print('client removed')
                        try:
                            self.handleMessage(json.loads(piece), conn)
                            print(f"[{addr}] {piece}")
                        except Exception as e: 
                            print(e)
                            print('Message couldnt be handled -> Removing client')
                            try:
                                connected = False
                                self.client_sockets.remove(conn)
                                print('client removed')
                            except ValueError as e:
                                print('could not remove client (not found)')
            except ConnectionResetError as e:
                connected = False
                print('Connection Error')
                try:
                    self.client_sockets.remove(conn)
                    print('client removed')
                except ValueError as e:
                    print('could not remove client (not found)')

        conn.close()

    def handleMessage(self, message, conn = None):
        if(message['type'] == 'HELLO'):
            self.message['type'] = 'WELCOME'
            self.message['data'] = str(self.client_sockets.index(conn)) # number of connection
            self.message['comment'] = str(self.client_sockets.index(conn) + 1)
            self.sendMessage(self.message, conn)
        elif(message['type'] == 'DIRECTION'):
            self.parent.current_mode.handleDirection(message['data'], self.client_sockets.index(conn))
        elif(message['type'] == 'CONFIRM'):
            self.parent.current_mode.handleConfirm(self.client_sockets.index(conn))
        elif(message['type'] == 'RETURN'):
            self.parent.current_mode.handleReturn()
        elif(message['type'] == 'MODE'):
            self.parent.setModeByName(message['data'])
        elif(message['type'] == 'MODES'):
            self.message['type'] = 'MODES'
            self.message['data'] = self.parent.getModes()
            self.message['comment'] = str(self.client_sockets.index(conn) + 1) # 'These are all the modes that are defined by the server'
            self.sendMessage(self.message, conn)
        elif(message['type'] == 'SETTINGS'):
            settings = json.loads(message['data'])
            self.parent.current_mode.handleSetting(settings)
            self.parent.display.setBrightness(settings['brightness'])
        elif(message['type'] == 'MODESETTINGS'):
            settings = json.loads(message['data'])
            self.parent.current_mode.handleModeSetting(settings)
    

    def sendMessage(self, message, conn = None):
        if(conn is None):
            for s in self.client_sockets:
                try:
                    s.send(json.dumps(message).encode(FORMAT))
                except Exception as e:
                    print('Message could not be sent -> Removing client')
                    self.client_sockets.remove(s)
        else:
            try:
                conn.send(json.dumps(message).encode(FORMAT))
            except Exception as e:
                self.client_sockets.remove(conn)
        #if(self.client_socket is None or self.addr is None):
        #    return False
        #self.client_socket.send(json.dumps(message).encode(FORMAT))

    ##Tuya Control Handle Functions:
    def onConnected(self):
        print('Tuya Control Connected')

    def onQRCode(self, url):
        qrcode_generate(url)

    def onReset(self, data):
        print('Tuya Reset:', data)

    def onDataPointSet(self, dps):
        print('DataPoints: ',dps)
        #functions...

        #ON/OFF
        if('101' in dps): #'1' is part of google home
            if(dps['101']):
                self.parent.setModeByName(self.parent.lastMode)
            else:
                self.parent.setModeByName('off')
        if('1' in dps): #'1' is part of google home
            if(dps['1']):
                self.parent.setModeByName(self.parent.lastMode)
            else:
                self.parent.setModeByName('off')
        #Brightness
        elif('102' in dps):
            self.parent.display.setBrightness(dps['102'])
        #Mode
        elif('103' in dps):
            self.parent.setModeByName(dps['103'])
        #Speed
        elif('104' in dps):
            self.parent.current_mode.handleSetting({'speed': dps['104'], 'size': self.parent.current_mode.size})
        #Size
        elif('106' in dps):
            self.parent.current_mode.handleSetting({'speed': self.parent.current_mode.size, 'size': dps['106']})
        #Button
        elif('105' in dps):
                self.parent.current_mode.handleConfirm()

        self.tuyaClient.push_dps(dps)
