import logging

from .vosk_text import *
from .pocketsphinx_kws import *
from .picovoice_kws import *
from piassistant.IauditoryCortexGateway import *
from .ear.ear import *

class AuditoryCortex(IauditoryCortexGateway):
    def __init__(self,*args,**kwargs):
        logging.info("Starting Auditory cortex...")
        self.useCmdInput = False
        self.ear = Ear(**kwargs)
        self.text = VoskText(self.ear, kwargs["voskModel"])
        if kwargs["KWS_engine"] == "pocketsphinx":
            self.kws = PocketsphinxKWS(self.ear,**kwargs)
        elif kwargs["KWS_engine"] == "picovoice":  
            self.kws = PicovoiceKWS(self.ear,**kwargs)
                
        logging.info("Auditory cortex ready")

    def listen(self,file=None,record=False,verbose=1):
        if self.useCmdInput:
            text = input("Geben sie eine Anweisung ein:")
            return [[{'text':text}], None]
        else:
            return self.text.listen(file=file,record=record,verbose=verbose)
            

    def wait(self):
        if self.useCmdInput == False:
            return self.kws.wait()
        else:
            return True

