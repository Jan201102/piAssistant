
from auditoryCortex.vosk_text import *
from auditoryCortex.pocketsphinx_kws import *

from IauditoryCortexGateway import *

class AuditoryCortex(IauditoryCortexGateway):
    def __init__(self,models,kws_model,name):
        self.text = VoskText(models)
        self.kws = PocketsphinxKWS(name = name, kws_model= kws_model)

    def listen(self,record=0,verbose=0):
        return self.text.listen(record,verbose)

    def wait(self):
        return self.kws.wait()


