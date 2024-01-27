import pyaudio
from piassistant.auditoryCortex.IearGateway import *
from piassistant.auditoryCortex.ear.AudioThread import *
from piassistant.auditoryCortex.ear.recorder import Recorder
import wave
import time


class Ear(IearGateway):
    FORMAT = pyaudio.paInt16
    CHUNK = 4096
    CHANNELS = 1
    p = pyaudio.PyAudio()

    def __init__(self, micId = None,  **kwargs):
        logging.info("starting Ear...")
        self.sampRate = 16000
        self.file = None
        self.recorder = Recorder(self.sampRate, self.CHANNELS, self.p.get_sample_size(self.FORMAT))

        if micId is not None:
            self.mic_id = micId
        else:
            for i in range(self.p.get_device_count()):
                try:
                    if self.p.is_format_supported(self.sampRate, input_device=i, input_format=self.FORMAT,
                                                  input_channels=self.CHANNELS):
                        print(self.p.get_device_info_by_index(i))
                except ValueError:
                    logging.debug("{} not supporting 16000khz".format(i))
            self.mic_id = int(input("please Input device index of preferred mic: "))

        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  input_device_index=self.mic_id,
                                  rate=int(self.sampRate),
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        logging.info("Ear Ready")
    def __del__(self):
        self.stream.close()

    def start_audio(self, file=None, record=False, timeout=0, threading=True, verbose=0):
        self.file = file
        self.recorder.new_record()
        if file is None:
            self.threading = threading
            self.record = record
            start = time.perf_counter()
            self.stream.start_stream()
            logging.debug('{} second[s] for opening audio stream'.format(time.perf_counter() - start))
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


        return self.recorder.save_recording()
