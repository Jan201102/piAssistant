from pocketsphinx.pocketsphinx import *

from os import path
from auditoryCortex.ear.ear import *
import time

class PocketsphinxKWS():
    def __init__(self,**kwargs):
        self.start_sec = 0
        self.kws_decoder = (kwargs)
        self.ear=Ear()

    @property
    def kws_decoder(self):
        return self.__kws_decoder
        
    @kws_decoder.setter
    def kws_decoder(self,kwargs):
        model = kwargs['kws_model']
        name = kwargs['name']
       # if threshold >= 40 or threshold < 0 :
        #    print("choose a sensitivity between 0 and 40")
         #   exit(0)
      #  threshold = 40-threshold
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(model,'hmm'))
        config.set_string('-dict', path.join(model,'model.dic'))
        config.set_string('-keyphrase',name)
        config.set_float('-kws_threshold', float(1e-20))
        self.__kws_decoder = Decoder(config)
        
    def wait(self):
        '''
        Erweitert Audio-backend.wait() um die für pocketahpinx nötigen Zeilen
        '''
        self.ear.start_audio(threading = False)
        self.kws_decoder.start_utt()
        
        self.kws_decoder.process_raw(self.ear.get_audio(),False,False)
        while self.kws_decoder.hyp() == None:
            self.kws_decoder.process_raw(self.ear.get_audio(),False,False)
        self.start_sec = time.perf_counter()
        self.kws_decoder.end_utt()
        print('{} kws decoder ende utt'.format(time.perf_counter()-self.start_sec))
        self.ear.stop_audio()
        print('{} sec  stoped audio -> wait() finished'.format(time.perf_counter()-self.start_sec))
        return True
