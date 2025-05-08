import logging
from pocketsphinx import *
import os
import time
import logging

class PocketsphinxKWS:
    def __init__(self, ear, sensitivity,**kwargs):
        logging.info("Loading pocketsphinx model...")
        self.start_sec = 0
        self.sensitivity = sensitivity
        self.kws_decoder = kwargs
        self.ear = ear
        logging.info("Done")

    @property
    def kws_decoder(self):
        return self.__kws_decoder

    @kws_decoder.setter
    def kws_decoder(self, kwargs):
        path = kwargs['pocketsphinxModel']
        name = kwargs['name']
        hmm = self.scan_dir_for_hmm_files(path)
        dictionary = self.scan_dir_for_dic_files(path)

        if hmm is None:
            raise ValueError('hmm not found for pocketsphinx')
        if dictionary is None:
            raise ValueError('dictionary for pocketsphinx not found')

        self.__kws_decoder = Decoder(hmm = hmm, dict = dictionary, keyphrase = name, kws_threshold = self.sensitivity)

    def scan_dir_for_hmm_files(self, path):
        required_files = {'feat.params', 'mdef', 'noisedict'}
        # Check if all required files exist in the current directory
        if required_files.issubset(set(os.listdir(path))):
            return path
        # Recursively check subdirectories
        elif self.has_subdirectories(path):
            for entry in os.scandir(path):
                if entry.is_dir():
                    hmm = self.scan_dir_for_hmm_files(entry.path)
                    if hmm is not None:
                        return hmm
        return None
        
    def scan_dir_for_dic_files(self, path):
        for entry in os.scandir(path):
            if entry.is_file() and entry.name.endswith(".dic"):
                return os.path.join(path, entry.name)
            elif entry.is_dir():
                result = self.scan_dir_for_dic_files(entry.path)
                if result:
                    return result
        return None

    @staticmethod        
    def has_subdirectories(folder_path):
        for entry in os.scandir(folder_path):
            if entry.is_dir():
                return True
        return False

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
