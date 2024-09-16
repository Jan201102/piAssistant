import pyttsx4
import logging

class TTS():
    def __init__(self):
        self.engine = pyttsx4.init()
        self.engine.setProperty('voice', 'german')
        self.engine.setProperty('rate', 150)

    def say(self, text):
        logging.debug(f"saying:{text}")
        self.engine.say(text)
        logging.debug("processing text to be spoken")
        self.engine.runAndWait()
        logging.debug("Done")