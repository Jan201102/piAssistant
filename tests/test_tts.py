import context
from piassistant.speechCenter.tts import TTS
import unittest
import signal

def timeout_handler(signum, frame):
    raise TimeoutError

class TestTTS(unittest.TestCase):
    def setUp(self):
        self.tts = TTS()
        
    def test_say(self):
        #check if TTS.say() finishes in reasonable time
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(15)
        try:
            self.tts.say("es wird zwischen 8,85 und 17,82 grad warm, bei 0,31 milimeter Niederschlag und einer durchschnittlichen Windgeschwindigkeit von 3,64 meter pro sekunde")
        except TimeoutError:
            self.fail("TTS.say() took too long to exceute")
            
        finally:
            signal.alarm(0)
        
        