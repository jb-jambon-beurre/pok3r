import socket
from threading import Thread

class Network(Thread):
#   Exemple de programme client-serveur:
#
# n = Network()
# choix = input("client/serveur? ")
# if choix == "client": # Mode client
#     n.connect(input("IP: "))
# else: # Mode serveur
#     n.listen() # On lance le serveur en ecoute
#
# # On donne une fonction à exécuter quand on reçoit un message avec le header "textemessagerie"
# n.handle_message("textemessagerie",
#     lambda msg: print("\n" + msg + "\n>>> ", end="")
# )
#
# while True: # Pour toujours
#     n.send("textemessagerie", input(">>> ")) # On envoie un message avec le header "textemessagerie"
# n.join() # On attend que le Thread se termine (probablement inutile avec une interface graphique)

    pending = []
    handles = {}
    host = ""
    port = 4242

    def __init__(self):
        Thread.__init__(self)
        self.running = False
        self.server = False
        self.connection = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip="", port=4242):
        self.host, self.port = ip, port
        self.server = False
        self.socket.connect((self.host, self.port))
        self.start()

    def listen(self, port=4242):
        self.host, self.port = "", port
        self.server = True
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.start()

    def run(self):
        self.running = True
        
        if self.server:
            while self.running:
                conn, addr = self.socket.accept()
                self.connection = conn
                with conn:
                    print('Connected by', addr)
                    for msg in self.pending:
                        conn.sendall(msg)
                    
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        self.handle_data(data)
                self.connection = False
        else:
            self.connection = self.socket
            for msg in self.pending:
                conn.sendall(msg)

            while self.running:
                data = self.socket.recv(1024)
                if data: self.handle_data(data)

    def send(self, message_type, message):
        data = (message_type + "\0" + message).encode('utf8')
        if self.connection:
            self.connection.send(data)
        else:
            self.pending.append(data)

    def stop(self):
        self.running = False

    def handle_message(self, message_type, callback):
        self.handles[message_type] = callback

    def handle_data(self, data):
        data = data.decode("utf8").split("\0")
        msg_type = data[0]
        msg = data[1]
        if msg_type in self.handles.keys():
            self.handles[msg_type](msg)
