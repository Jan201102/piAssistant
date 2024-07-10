import context
from piassistant.speechCenter import speechCenter
import unittest
import signal

def timeout_handler(signum, frame):
    raise TimeoutError

class TestSpeechCenter(unittest.TestCase):
    def setUp(self):
        self.speechCenter = speechCenter.SpeechCenter()
        
    def test_say(self):
        #check if TTS.say() finishes in reasonable time
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(15)
        try:
            self.speechCenter.say("test")
        except TimeoutError:
            self.fail("TTS.say() took too long to exceute")
            
        finally:
            signal.alarm(0)
        
        