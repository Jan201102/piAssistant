from RealtimeTTS import TextToAudioStream, SystemEngine
import logging

class TTS():
    def __init__(self,voice:str = "Hedda",speed:int = 150):
        """
        Initializes the TTS engine with the specified voice and speed.
        Args:
            voice (str, optional): voice name. Defaults to "Hedda".
            speed (int, optional): rate of speech in words per minute. Defaults to 120.
        """
        logging.info("Initializing TTS engine")
        self.engine = SystemEngine(voice)
        self.engine.set_voice_parameters(rate = speed)
        self.stream = TextToAudioStream(self.engine)
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
        self.stream.play()
        logging.debug("Done")

    def say_async(self,text:str):
        """
        Converts the given text into speech and plays it asynchronously.
        Args:
            text (str): The text to be converted into speech.
        """
        logging.debug(f"saying:{text}")
        self.stream.feed(text)
        logging.debug("processing text to be spoken")
        if self.stream.is_playing() is False:
            self.stream.play_async()
        logging.debug("Done")