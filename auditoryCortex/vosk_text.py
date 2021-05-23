from vosk import Model, KaldiRecognizer, SetLogLevel
from os import path
from auditoryCortex.ear.ear import *
import json
import time
class VoskText():
    def __init__(self, models, **kwargs):
        self.ear = Ear()
        SetLogLevel(0)
        for model in models:
            if not path.exists(model):
                print("cant't find: " +model)
                exit(0)
        self.decoder =models

    @property
    def decoder(self):
        return self.__decoder
    
    @decoder.setter
    def decoder(self,model_path):
        self.__decoder = []
        for path in model_path:
            model = Model(path)
            self.__decoder.append(KaldiRecognizer(model,float(self.ear.sampRate)))
        
    def listen(self, record = False, verbose = 1,file=None):
        #if verbose : print('{} sec listen started'.format(time.perf_counter()-self.ear.start_sec))
        self.ear.start_audio(record=record, threading=True, verbose= verbose,file=file)
        #if verbose: print('{} sec to react'.format(time.perf_counter()-self.start_sec))
        data = self.ear.get_audio()
        run = True
        partial_results = []
        for _ in self.decoder:
            partial_results.append(None)
        while run:
            for i, dec in enumerate(self.decoder):
                if not dec.AcceptWaveform(data):
                    partial_results[i] = dec.PartialResult()
                    if verbose: print(partial_results[i])
                else:
                    run = False
            data = self.ear.get_audio()
        print(record)
        wav_file = self.ear.stop_audio(verbose)
        return [[json.loads(dec.FinalResult()) for dec in self.decoder],wav_file]

