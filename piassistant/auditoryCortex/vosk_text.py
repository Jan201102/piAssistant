from vosk import Model, KaldiRecognizer, SetLogLevel
import logging
import time
from os import path
import json


class VoskText():
    def __init__(self,ear, models, **kwargs):
        logging.info("loading vosk model...")
        self.ear = ear
        SetLogLevel(-1)
        for model in models:
            if not path.exists(model):
                logging.error("cant't find: " +model)
                exit(0)
        self.decoder =models
        logging.info("Done.")

    @property
    def decoder(self):
        return self.__decoder
    
    @decoder.setter
    def decoder(self,model_path):
        self.__decoder = []
        for path in model_path:
            model = Model(path)
            self.__decoder.append(KaldiRecognizer(model,float(self.ear.sampRate)))
        
    def listen(self, verbose = 1):
        data = self.ear.get_audio()
        run = True
        partial_results = []
        for _ in self.decoder:
            partial_results.append(None)
        while run:
            for i, dec in enumerate(self.decoder):
                if not dec.AcceptWaveform(data):
                    partial_results[i] = dec.PartialResult()
                    logging.debug(partial_results[i])
                else:
                    run = False
            data = self.ear.get_audio()
        return [[json.loads(dec.FinalResult()) for dec in self.decoder],wav_file]

