from Blockchain.Core.Network.connection import Node

class Net_sync:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def spinUPTheServer(self):
        self.server=Node(self.host, self.port)
        self.server.startServer()
        print('Status: Server started')
        print(f"[Listening] at {self.host}:{self.port}")