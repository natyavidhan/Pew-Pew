import socket
import json

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.user = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        data = self.client.recv(2048).decode()
        print(data)
        return data

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            response = self.client.recv(2048).decode()
            return response
        except socket.error as e:
            return str(e)