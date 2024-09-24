import pyaudio
from piassistant.auditoryCortex.IearGateway import *
from piassistant.auditoryCortex.ear.AudioThread import *
from piassistant.auditoryCortex.ear.recorder import Recorder
import wave
import time


class Ear(IearGateway):
    FORMAT = pyaudio.paInt16
    CHUNK = 512
    CHANNELS = 1
    p = pyaudio.PyAudio()

    def __init__(self, **kwargs):
        logging.info("starting Ear...")
        self.sampRate = 16000
        self.file = None
        self.recorder = Recorder(self.sampRate, self.CHANNELS, self.p.get_sample_size(self.FORMAT))
        return
        
    def open_audio_stream(self):
        logging.debug("Opening audio stream")
        numFails = 0
        while numFails <10:
            try:
                self.stream = self.p.open(format=self.FORMAT,
                                        channels=self.CHANNELS,
                                        rate=int(self.sampRate),
                                        input=True,
                                        frames_per_buffer=self.CHUNK)
                break
            except OSError as e:
                numFails += 1
                if numFails >= 10:
                    logging.error(e)
                    raise(e)
            logging.debug("Failed to open audiostream retrying...")
                
        logging.debug("Audio stream opened")
        
        
    def __del__(self):
        self.stream.close()

    def start_audio(self, file=None, record=False, timeout=0, threading=True, verbose=0):
        self.open_audio_stream()
        self.file = file
        self.recorder.new_record()
        if file is None:
            self.threading = threading
            self.record = record
            self.stream.start_stream()
            if threading:
                self.thread = AudioThread(self.stream, self.CHUNK, timeout, self.sampRate)
        else:
            self.file = wave.open(file, 'rb')

    def get_audio(self):
        if self.file is None:
            if self.threading:
                data = self.thread.get()
            else:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            if self.record:
                self.recorder.record(data)
        else:
            data = self.file.readframes(1024)
        return data

    def stop_audio(self, verbose=0):
        if self.file is None:
            if self.threading:
                self.thread.stop(verbose)
            self.stream.stop_stream()
        self.stream.close()
        return self.recorder.save_recording()
