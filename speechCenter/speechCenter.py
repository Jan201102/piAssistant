from IspeechCenterGateway import IspeechCenterGateway
from speechCenter.tts import *


class SpeechCenter(IspeechCenterGateway):
    def __init__(self):
        self.tts = TTS()

    def say(self,text):
        self.tts.say(text)
