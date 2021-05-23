from IspeechCenterGateway import IspeechCenterGateway
from tts import *
class speechCenter(IspeechCenterGateway):
    def __init__(self):
        self.tts = TTS()

    def say(self,text):
        self.tts.say(text)
