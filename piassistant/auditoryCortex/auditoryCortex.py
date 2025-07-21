import logging

from .vosk_text import *
from piassistant.IauditoryCortexGateway import *
from .ear.ear import *


class AuditoryCortex(IauditoryCortexGateway):
    def __init__(self,*args,**kwargs):
        logging.info("Starting Auditory cortex...")
        self.useCmdInput = False
        self.ear = Ear(**kwargs)
        self.text = VoskText(self.ear, kwargs["voskModel"])
        if kwargs["KWS_engine"] == "pocketsphinx":
            from .pocketsphinx_kws import PocketsphinxKWS
            self.kws = PocketsphinxKWS(self.ear,**kwargs)
        elif kwargs["KWS_engine"] == "openwakeword":
            from .openwakeword import OpenWakeWordDetector
            self.kws = OpenWakeWordDetector(self.ear,**kwargs)
                
        logging.info("Auditory cortex ready")

    def listen(self,file=None,record=False,verbose=1):
        if self.useCmdInput:
            text = input("Geben sie eine Anweisung ein:")
            return [[{'text':text}], None]
        else:
            self.ear.start_audio(file = file, record=record)
            result = self.text.listen(verbose=verbose)
            self.ear.stop_audio()
            return result

    def wait(self):
        if self.useCmdInput == False:
            self.ear.start_audio(threading=False)
            self.kws.wait()
            self.ear.stop_audio()
            return True
        return True
        
    def wait_then_listen(self, record=False, verbose=1):
        if self.useCmdInput:
            text = input("Geben sie eine Anweisung ein:")
            return [[{'text':text}], None]
        else:
            self.ear.start_audio(threading=False)
            self.kws.wait()
            if record:
                self.ear.start_recording()
            result = self.text.listen( verbose=verbose)
            self.ear.stop_audio(verbose=verbose)
            return result
