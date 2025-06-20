from RealtimeTTS import TextToAudioStream, SystemEngine, PiperVoice, PiperEngine
import logging

class TTS():
    def __init__(self,voice:str = "German",speed:int = 150,piper_model:str="",piper_config:str="",piper_path:str="",**kwargs):
        """
        Initializes the TTS engine with the specified voice and speed.
        Args:
            voice (str, optional): voice name. Defaults to "Hedda".
            speed (int, optional): rate of speech in words per minute. Defaults to 120.
            piper_model (str, optional): path to the piper model file. Defaults to "".
            piper_config (str, optional): path to the piper config file. Defaults to "".
            piper_path (str, optional): path to the piper executable. Defaults to "".
        """
        logging.info("Initializing TTS engine")
        self.engine = SystemEngine(voice)
        if piper_model and piper_config and piper_path:
            logging.info("Using Piper TTS engine")
            self.engine = PiperEngine(piper_path=piper_path, voice=PiperVoice(model_file=piper_model, config_file=piper_config), debug=True)
        else:
            logging.info("Using System TTS engine")
            self.engine = SystemEngine(voice)
            self.engine.set_voice_parameters(rate = speed)
        self.stream = TextToAudioStream(self.engine,frames_per_buffer=256,level = logging.getLogger().getEffectiveLevel()) #frames_per_buffer=256 avoids stuttering on rpi
        logging.info("Done")

    def say(self,text:str):
        """
        Converts the given text into speech and plays it.
        Args:
            text (str): The text to be converted into speech.
        """
        logging.debug(f"saying:{text}")
        self.stream.feed(text)
        logging.debug("processing text to be spoken")
        self.stream.play(fast_sentence_fragment_allsentences=True)
        logging.debug("Done")

    def say_async(self,text:str,**kwargs):
        """
        Converts the given text into speech and plays it asynchronously.
        Args:
            text (str): The text to be converted into speech.
        """
        logging.debug(f"saying:{text}")
        self.stream.feed(text)
        if self.stream.is_playing() is False:
            self.stream.play_async(fast_sentence_fragment_allsentences=True,**kwargs)