from main import *
a = Main(name='computer', models=['C:/Users/lukas/Downloads/vosk-model'], kws_model ='C:/Users/lukas/Downloads/cmusphinx-cont-de',sensitivity=100)
#print(a.listen(file='6061421695164418587.wav'))

a.start()

