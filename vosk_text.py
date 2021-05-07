from vosk import Model, KaldiRecognizer, SetLogLevel
from os import path
from Assistant_audio_backend import *
import json
class VoskText(Audio_backend):
    def __init__(self, model, **kwargs):
        super(VoskText,self).__init__(**kwargs)
        
        SetLogLevel(0)
        if not path.exists(model):
            print("cant't find the model in your specified directory")
            exit(0)
        self.decoder =model

    @property
    def decoder(self):
        return self.__decoder
    
    @decoder.setter
    def decoder(self,model_path):
        model = Model(model_path)
        #print(self.sampRate)
        self.__decoder = KaldiRecognizer(model,float(self.sampRate))
        
    def listen(self, record = False, verbose = 0):
        if not verbose : print('{} sec listen started'.format(time.perf_counter()-self.start_sec))
        self.start_audio(record, threading=False, verbose= verbose)
        if not verbose: print('{} sec to react'.format(time.perf_counter()-self.start_sec))
        data = self.get_audio()
        while not self.decoder.AcceptWaveform(data):
            partial = self.decoder.PartialResult()
            if not verbose: print(partial)
            data = self.get_audio()
            
        self.stop_audio(verbose)
        return json.loads(self.decoder.FinalResult())