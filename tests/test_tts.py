import unittest
import multiprocessing
from piassistant.speechCenter.tts import TTS
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run_tts_in_process(text):
    tts = TTS()  # TTS-Instanz im neuen Prozess erstellen
    tts.say(text)

class TestTTS(unittest.TestCase):
    def test_say_process(self):
        # Prozess erstellen
        tts_process = multiprocessing.Process(target=run_tts_in_process, args=("George esra war ein singer,songwriter",))

        # Prozess starten
        tts_process.start()

        # Warten bis der Prozess fertig ist (mit Timeout)
        tts_process.join(timeout=20)  # Timeout von 15 Sekunden
        if tts_process.is_alive():
            tts_process.terminate()  # Prozess beenden, falls er hängt
            self.fail("TTS.say() hat zu lange gebraucht")

        # Test erfolgreich, wenn der Prozess abgeschlossen ist
        self.assertFalse(tts_process.is_alive(), "Der TTS-Prozess sollte beendet sein")
    
    def test_say_async(self):
        tts = TTS()
        time.sleep(2)
        tts.say_async("es ist wolkig bei einer Temperatur von 16,0 grad, 22,2 milimeter Niederschlag" \
                            " und einer Windgeschwindigkeit von 4,22 meter pro sekunde")
        time.sleep(5)
        tts=None
    
    def test_say(self):
        tts = TTS()
        time.sleep(2)
        tts.say("warm up")
        time.sleep(10)
        tts.say("es ist wolkig bei einer Temperatur von 16.0 grad, 22.2 milimeter Niederschlag" \
                            " und einer Windgeschwindigkeit von 4.22 meter pro sekunde")
        time.sleep(10)
        tts=None



