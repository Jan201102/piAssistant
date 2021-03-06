import logging
from pocketsphinx.pocketsphinx import *
import os
import time


class PocketsphinxKWS:
    def __init__(self, ear, **kwargs):
        self.start_sec = 0
        self.sensitivity = kwargs['sensitivity']
        self.kws_decoder = kwargs
        self.ear = ear

    @property
    def kws_decoder(self):
        return self.__kws_decoder

    @kws_decoder.setter
    def kws_decoder(self, kwargs):
        path = kwargs['pocketsphinxModel']
        name = kwargs['name']
        hmm = None
        dictionary = None
        for entry in os.scandir(path):
            if entry.is_dir():
                if 'feat.params' and 'mdef' and 'noisedict' in os.listdir(path + "/" + entry.name):
                    hmm = os.path.join(path, entry.name)
                if ".dic" in entry.name:
                    dictionary = os.path.join(path, entry.name)
            else:
                if ".dic" in entry.name:
                    dictionary = os.path.join(path, entry.name)

        if hmm is None:
            raise ValueError('hmm not found for pocketsphinx')
        if dictionary is None:
            raise ValueError('dictionary for pocketsphinx not found')

        config = Decoder.default_config()
        config.set_string('-hmm', hmm)
        config.set_string('-dict', dictionary)
        config.set_string('-keyphrase', name)
        config.set_float('-kws_threshold', self.sensitivity)
        config.set_string('-logfn', 'nul')
        self.__kws_decoder = Decoder(config)

    def wait(self):
        self.ear.start_audio(threading=False)
        self.kws_decoder.start_utt()

        self.kws_decoder.process_raw(self.ear.get_audio(), False, False)
        while self.kws_decoder.hyp() == None:
            self.kws_decoder.process_raw(self.ear.get_audio(), False, False)
        self.start_sec = time.perf_counter()
        self.kws_decoder.end_utt()
        logging.debug('{} kws decoder ende utt'.format(time.perf_counter() - self.start_sec))
        self.ear.stop_audio()
        logging.debug('{} sec  stoped audio -> wait() finished'.format(time.perf_counter() - self.start_sec))
        return True

    @property
    def sensitivity(self):
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        value = value / 2
        if value < 1:
            value = 1
        self.__sensitivity = float(10 ** -value)
