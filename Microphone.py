import sounddevice as sd
import numpy

import time

class Mic():
    def __init__(self):
        print("Başladı")
        self.sample_rate = 44100

        self.data = numpy.array([])
        self.stream = sd.InputStream(samplerate=self.sample_rate, callback=self.callback)

    def callback(self, indata, frames, time, status):
        if status:
            print(status)

        new_data = numpy.append(self.data, indata)
        self.data = new_data
        
    def start_stream(self):
        self.data = numpy.array([])
        self.stream.start()
    
    def stop_stream(self):
        self.stream.stop()
    
    def play_data(self, data):
        print("Oynatılıyor...")
        sd.play(data, samplerate=(self.sample_rate * 2))
