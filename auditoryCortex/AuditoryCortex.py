
from auditoryCortex.vosk_text import *
from auditoryCortex.pocketsphinx_kws import *

from IauditoryCortexGateway import *

class AuditoryCortex(IauditoryCortexGateway):
    def __init__(self,models,kws_model,name):
        self.text = VoskText(models)
        self.kws = PocketsphinxKWS(name = name, kws_model= kws_model)

    def listen(self,file=None,record=False,verbose=1):
        return self.text.listen(file=file,record=record,verbose=verbose)

    def wait(self):
        return self.kws.wait()


