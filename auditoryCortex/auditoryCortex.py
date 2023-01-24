import logging

from auditoryCortex.vosk_text import *
from auditoryCortex.pocketsphinx_kws import *
from IauditoryCortexGateway import *
from auditoryCortex.ear.ear import *

class AuditoryCortex(IauditoryCortexGateway):
    def __init__(self,*args,**kwargs):
        logging.info("Starting Auditory cortex...")
        self.ear = Ear(**kwargs)
        if self.ear.mic_id != None:
            self.text = VoskText(self.ear, kwargs["voskModel"])
            self.kws = PocketsphinxKWS(self.ear,**kwargs)
        logging.info("Auditory cortex ready")

    def listen(self,file=None,record=False,verbose=1):
        if self.ear.mic_id != None:
            return self.text.listen(file=file,record=record,verbose=verbose)
        else:
            text = input("Geben sie eine Anweisung ein:")
            return [[{'text':text}], None]

    def wait(self):
        if self.ear.mic_id != None:
            return self.kws.wait()
        else:
            return True

