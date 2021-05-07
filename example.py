from vosk_text import *
from pocketsphinx_kws import *

class VAssistant(VoskText,PocketsphinxKWS):
    pass

a = VAssistant(name='computer',model='vosk-model',kws_model = 'cont-de',audio=True)

while True:
    print('listening...')
    if a.wait():
        command = a.listen()
        print(command['text'])