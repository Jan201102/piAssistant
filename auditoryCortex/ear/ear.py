import pyaudio
from auditoryCortex.IearGateway import *
from auditoryCortex.ear.AudioThread import *
import wave
import time


class Ear(IearGateway):
    FORMAT = pyaudio.paInt16
    CHUNK = 4096
    CHANNELS = 1
    p = pyaudio.PyAudio()

    def __init__(self, **kwargs):
        self.mic_id = None
        self.sampRate = 16000
        self.file=None
        for i in range(self.p.get_device_count()):
            try:
                if self.p.is_format_supported(self.sampRate,input_device=i,input_format=self.FORMAT,input_channels=self.CHANNELS):
                    self.mic_id = i
            except ValueError:
                pass
        if self.mic_id == None:
            print('Attention: no mic plugged in!')

    def start_audio(self,file=None, record=False, timeout=0, threading=True, verbose=0):

        if file == None:
            print('start_stream')
            self.threading = threading
            self.record = record
            start = time.perf_counter()
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      input_device_index=self.mic_id,
                                      rate=int(self.sampRate),
                                      input=True,
                                      frames_per_buffer=self.CHUNK)

            self.stream.start_stream()
            if not verbose: print('{} second[s] for opening audio stream'.format(time.perf_counter() - start))
            self.frames = []
            if threading == True:
                self.thread = AudioThread(self.stream, self.CHUNK, timeout, self.sampRate)
        else:
            self.file = wave.open(file, 'rb')
    def get_audio(self):
        if self.file == None:
            if self.threading == True:
                data = self.thread.get()
            else:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            if self.record:
                self.frames.append(data)
        else:
            data=self.file.readframes(1024)
        return data

    def stop_audio(self,verbose=0):
        print(self.file)
        if self.file==None:

            if self.threading == True:
                self.thread.stop(verbose)
            self.stream.stop_stream()
            self.stream.close()

            if len(self.frames) != 0:
                wav = hash(tuple(self.frames))
                # print('hash: {}'.format(wav))
                filename = str(wav) + ".wav"

                # write wav
                wf = wave.open(filename, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.sampRate)
                wf.writeframes(b''.join(self.frames))
                wf.close()

                return filename
        return


