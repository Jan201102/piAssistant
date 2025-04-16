import unittest
import multiprocessing
from piassistant.speechCenter.tts import TTS
import time

def run_tts_in_process(text):
    tts = TTS()  # TTS-Instanz im neuen Prozess erstellen
    tts.say(text)

class TestTTS(unittest.TestCase):
    def test_say(self):
        # Prozess erstellen
        tts_process = multiprocessing.Process(target=run_tts_in_process, args=("es wird zwischen 8,85 und 17,82 grad warm",))

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
        tts.say_async("es wird zwischen 8,85 und 17,82 grad warm")
        time.sleep(5)
        tts=None
        

if __name__ == "__main__":
    unittest.main()



