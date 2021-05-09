from main import *
a = PiAssistant(name='computer',models=['/home/pi/piAssistant/vosk-model'],kws_model = '/home/pi/jasper_v3/cont-de')

while True:
    print('listening...')
    if a.wait():
        command = a.listen(record=True)
        print(command)
        #'/home/pi/piAssistant/vosk-model',