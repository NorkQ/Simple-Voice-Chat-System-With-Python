import socket
import threading as th
import time
from Microphone import Mic
import numpy as np
import pickle
import struct
from Message import Message

class Server():
    def __init__(self):
        self.bind_ip = "192.168.1.24"
        self.bind_port = 3333

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.bind_ip, self.bind_port))

        self.server.listen(10)
        
        self.clients = []

        th.Thread(target=self.find_client).start()
    
    def find_client(self):
        while True:
            print("Client bekleniyor...")
            client, addr = self.server.accept()
            print(f"Client accepted - ({addr[0]}:{addr[1]})")
            self.clients.append(client)

            id = (len(self.clients) - 1)

            print(f"Bağlanan client ID : {id}")

            th.Thread(target=self.take_message, args=(id,)).start()

            client.sendall(struct.pack('>I', len(bytes("ID-"+str(id), "utf-8"))))
            client.sendall(bytes("ID-"+str(id), "utf-8"))
    
    def take_message(self, id):
        while True:
            data_size = struct.unpack('>I', self.clients[id].recv(4))[0]
            received_payload = b""
            reamining_payload_size = data_size
            while reamining_payload_size != 0:
                received_payload += self.clients[id].recv(reamining_payload_size)
                reamining_payload_size = data_size - len(received_payload)
            
            data = pickle.loads(received_payload)
            print(len(data.data))
            self.send_message(data.data, int(data.id))
        
    
    def send_message(self, message, client_id):
        serialized_data = pickle.dumps(Message(message, client_id))

        for i in range(0, len(self.clients)):
            if i != client_id:
                self.clients[i].sendall(struct.pack('>I', len(serialized_data)))
                self.clients[i].sendall(serialized_data)


server = Server()
