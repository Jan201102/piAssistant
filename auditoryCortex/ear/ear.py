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
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] == 1:
                self.mic_id = i
                self.sampRate = dev['defaultSampleRate']
        if self.mic_id == None:
            print('Attention: no mic plugged in!')
        #self.engine = pyttsx3.init()
        #self.engine.setProperty('voice', 'german')
        #self.engine.setProperty('rate', 150)

   # def say(self, text):
    #    self.engine.say(text)
     #   self.engine.runAndWait()

    def start_audio(self, record=False, timeout=0, threading=True, verbose=0):
        '''
        Erzeugt einen pyaduio-stream zu [device].
        '''
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

    def get_audio(self):
        if self.threading == True:
            data = self.thread.get()
        else:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        if self.record:
            self.frames.append(data)
        return data

    def stop_audio(self,verbose=0):
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


    @staticmethod
    def play_wave(file):
        CHUNK = 1024
        p = pyaudio.PyAudio()
        'open wave file'
        wf = wave.open(file, 'rb')

        'open stream'
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        'play audio'
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)

        'stop stream'
        stream.stop_stream()
        stream.close()