import pyttsx3
import logging

class TTS():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'german')
        self.engine.setProperty('rate', 150)

    def say(self, text):
        logging.debug(f"saying:{text}")
        self.engine.say(text)
        self.engine.runAndWait()
        logging.debug("Done")