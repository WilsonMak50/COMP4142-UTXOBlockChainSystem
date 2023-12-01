import socket
class Node:
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.ADDR = (self.host, self.port)

    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.listen()