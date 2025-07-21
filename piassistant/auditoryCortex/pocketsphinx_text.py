'''
CURRENTLY NOT MAINTAINED
'''
from pocketsphinx.pocketsphinx import *

from os import path,mkdir


class PocketsphinxText():
    def __init__(self,ear, model, **kwargs):
        self.ear=ear
        if path.exists(model):
            self.model = model
        else:
            print("can't find model")
            exit(0)
            
        self.storage_dir = path.join(self.model,'data/unchecked_wav')
        self.data_dir = path.join(self.model,'data')
        if not path.exists(self.data_dir):
            mkdir(self.data_dir)
            mkdir(path.join(self.model,'data/checked_wav'))
            mkdir(self.storage_dir)
        self.decoder = self.model 
        
        super(PocketsphinxText,self).__init__(**kwargs)   
        
    @property
    def decoder(self):
        return self.__decoder
    
    @decoder.setter
    def decoder(self,model_path):
        config = Decoder.default_config()
        config.set_string('-hmm', path.join(model_path,'hmm'))
        config.set_string('-dict', path.join(model_path,'model.dic'))
        config.set_string('-lm',path.join(model_path,'model.lm.bin'))
        self.__decoder = Decoder(config)
        
    
    def listen(self,sec):

        self.decoder.start_utt()
        data = self.ear.get_audio()

        while data != None:
            self.decoder.process_raw(data,False,False)
            data = self.ear.get_audio()
        
        self.decoder.end_utt()
        
        return([seg.word for seg in self.decoder.seg()])

