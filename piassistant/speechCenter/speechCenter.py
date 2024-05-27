from piassistant.IspeechCenterGateway import IspeechCenterGateway
from piassistant.speechCenter.tts import TTS


class SpeechCenter(IspeechCenterGateway):
    def __init__(self):
        self.tts = TTS()

    def say(self,text):
        self.tts.say(text)
