import threading as th
import socket
import numpy as np
from Microphone import Mic
from pynput.keyboard import Listener, Key
import pickle
from Message import Message
import struct

mic = Mic()

class Client():
    def __init__(self):
        self.target_host = "192.168.1.24"
        self.target_port = 3333
        self.received_data = np.array([])
        self.data_to_send = np.array([])
        self.id = 0
        

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.target_host,self.target_port))

        th.Thread(target=self.take_message).start()
        th.Thread(target=self.key_trigger).start()
    
    def key_trigger(self):
        with Listener(on_press=self.key_press) as listener:
            listener.join()
    
    def take_message(self):    
        while True:
            data_size = struct.unpack('>I', self.server.recv(4))[0]
            received_payload = b""
            reamining_payload_size = data_size
            while reamining_payload_size != 0:
                received_payload += self.server.recv(reamining_payload_size)
                reamining_payload_size = data_size - len(received_payload)
            
            if b"ID-" in received_payload:
                self.id = received_payload.decode("utf-8").strip("ID-")
                print(f"ID:{self.id}")
            else:
                data = pickle.loads(received_payload)
                self.received_data = data.data
                print(len(self.received_data))
                mic.play_data(self.received_data)
    
    def send_message(self, message, client_id):
        serialized_data = pickle.dumps(Message(message, client_id))
        self.server.sendall(struct.pack('>I', len(serialized_data)))
        self.server.sendall(serialized_data)
        print("Mesaj gönderildi.")
        
    def key_press(self, key):
        if hasattr(key, 'char'):
            if key.char.lower() == "c":
                if not mic.stream.active:
                    mic.start_stream()
                    print("Mikrofon aktif edildi.")
                
                elif mic.stream.active:
                    mic.stop_stream()
                    print("Mikrofon pasif edildi.")
                    self.data_to_send = mic.data
                    self.send_message(self.data_to_send, self.id)
        else:
            print("Başka bir tuşa basıldı.")

client = Client()
