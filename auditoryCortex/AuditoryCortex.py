from auditoryCortex.vosk_text import *
from auditoryCortex.pocketsphinx_kws import *
from IauditoryCortexGateway import *
from auditoryCortex.ear.ear import *

class AuditoryCortex(IauditoryCortexGateway):
    def __init__(self,models,kws_model,name):
        self.ear = Ear()
        if self.ear.mic_id != None:
            self.text = VoskText(models,self.ear)
            self.kws = PocketsphinxKWS(self.ear, name = name, kws_model= kws_model)

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

