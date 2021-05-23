from abc import ABC

class IspeechCenterGateway(ABC):
    def __init__(self):
        pass

    def say(self,text):
        '''
        :param text: text the TTS-engine should output
        :return: None
        '''
        pass

    def play(self,file: str):
        '''
        :param file: the name of the file that the function plays. At the Moment only .wav-files are supported
        :return: None
        '''
        pass
