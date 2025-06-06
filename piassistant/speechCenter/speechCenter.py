from piassistant.IspeechCenterGateway import IspeechCenterGateway
from piassistant.speechCenter.tts import TTS


class SpeechCenter(IspeechCenterGateway):
    def __init__(self,**kwargs):
        self.tts = TTS(**kwargs)

    def say(self,text):
        self.tts.say(text)
    
    def say_async(self,text,**kwargs):
        self.tts.say_async(text,**kwargs)
