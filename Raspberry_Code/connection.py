import time, threading
import json
import socket

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = '{type:"DISCONNECT"'
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
        server_socket.bind(("0.0.0.0", 8942))
        server_socket.listen(2)
        while(True):
            (client_socket, addr) = server_socket.accept()
            thread = threading.Thread(target=self.handleClient, args=(client_socket, addr))
            thread.start()

    def handleClient(self, conn, addr):
        print(f"[NEW CONNECTION] from: {addr} | Total Connections: {threading.activeCount() - 3}")
        self.client_sockets.append(conn)
        connected = True
        while connected:
            #msg_length = conn.recv(HEADER)
            #if msg_length:
            #    print(msg_length)
            #    msg_length = int.from_bytes(msg_length, byteorder='little', signed=False)
            #    msg_length = int(msg_length)
            #    print(msg_length)
            msg = ""
            while True:
                msg += conn.recv(1024).decode(FORMAT)
                pieces = msg.split(SEPARATOR)
                msg = pieces.pop()
                for piece in pieces:
                    if(piece.startswith(DISCONNECT_MESSAGE) or not piece):
                        connected = False
                        self.client_sockets.remove(conn)
                    try:
                        self.handleMessage(json.loads(piece), conn)
                        print(f"[{addr}] {piece}")
                    except:
                       print('Message couldnt be handled')
                       pass
        conn.close()

    def handleMessage(self, message, conn = None):
        if(message['type'] == 'HELLO'):
            self.message['type'] = 'WELCOME'
            self.message['data'] = str(self.client_sockets.index(conn)) # number of connection
            self.message['comment'] = str(self.client_sockets.index(conn) + 1)
            self.sendMessage(self.message, conn)
        elif(message['type'] == 'DIRECTION'):
            self.parent.current_mode.handleDirection(message['data'])
        elif(message['type'] == 'CONFIRM'):
            self.parent.current_mode.handleConfirm()
        elif(message['type'] == 'RETURN'):
            self.parent.current_mode.handleReturn()
        elif(message['type'] == 'MODE'):
            self.parent.setModeByName(message['data'])
        elif(message['type'] == 'MODES'):
            self.message['type'] = 'MODES'
            self.message['data'] = self.parent.getModes()
            self.message['comment'] = str(self.client_sockets.index(conn) + 1) # 'These are all the modes that are defined by the server'
            self.sendMessage(self.message)
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
                s.send(json.dumps(message).encode(FORMAT))
        else:
            conn.send(json.dumps(message).encode(FORMAT))
        #if(self.client_socket is None or self.addr is None):
        #    return False
        #self.client_socket.send(json.dumps(message).encode(FORMAT))

    