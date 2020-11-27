import time, threading
import json
import socket

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = '{type:"DISCONNECT"'

class Connection(threading.Thread):
    def __init__(self, p):
        super(Connection, self).__init__()
        self.parent = p
        self.setDaemon(True)
        self.message = {"type": "WELCOME", "data": "", "comment": ""}

    def run(self):
        print("[STARTING] Server is starting")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", 8942))
        server_socket.listen(1)
        while(True):
            (self.client_socket, self.addr) = server_socket.accept()
            thread = threading.Thread(target=self.handleClient, args=(self.client_socket, self.addr))
            thread.start()

    def handleClient(self, conn, addr):
        print(f"[NEW CONNECTION] from: {addr} | Total Connections: {threading.activeCount() - 3}")
        connected = True
        while connected:
            #msg_length = conn.recv(HEADER)
            #if msg_length:
            #    print(msg_length)
            #    msg_length = int.from_bytes(msg_length, byteorder='little', signed=False)
            #    msg_length = int(msg_length)
            #    print(msg_length)
            msg = conn.recv(2048).decode(FORMAT)
            if(msg.startswith(DISCONNECT_MESSAGE) or not msg):
                connected = False
            try:
                self.handleMessage(json.loads(msg))
                print(f"[{addr}] {msg}")
            except:
                pass
            
        conn.close()

    def handleMessage(self, message):
        print(message)
        if(message['type'] == 'HELLO'):
            self.message['type'] = 'WELCOME'
            self.message['data'] = ''
            self.message['comment'] = ''
            self.sendMessage(self.message)
        elif(message['type'] == 'DIRECTION'):
            self.parent.current_mode.handleDirection(message['data'])
        elif(message['type'] == 'CONFIRM'):
            self.parent.current_mode.handleConfirm()
        elif(message['type'] == 'RETURN'):
            self.parent.current_mode.handleReturn()
        elif(message['type'] == 'MODE'):
            self.parent.setModeByName(message['data'])
            self.message['type'] = 'MODE'
            self.message['data'] = self.parent.current_mode.getName()
            self.message['comment'] = 'Selected mode'
            self.sendMessage(self.message)
        elif(message['type'] == 'MODES'):
            self.message['type'] = 'MODES'
            self.message['data'] = self.parent.getModes()
            self.message['comment'] = 'These are all the modes that are defined by the server'
            self.sendMessage(self.message)
    

    def sendMessage(self, message):
        if(self.client_socket is None or self.addr is None):
            return False
        self.client_socket.send(json.dumps(message).encode(FORMAT))

    