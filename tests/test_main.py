import unittest
import context
from piassistant.main import Main
import signal
import os
import sys

def timeout_handler(signum, frame):
    raise TimeoutError

class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.assistant = Main(configFile=os.path.join(sys.path[0],"config.json"))
                            
    def test_run_mastermodel(self):
        prediction = self.assistant.run_mastermodel("dimme die stehlampe auf sechzig prozent")
        self.assertEqual("hue.setlights({'stehlampe':60})", prediction.replace(" ", ""))
        prediction = self.assistant.run_mastermodel("schalte die stehlampe aus")
        self.assertEqual("hue.setlights({'stehlampe':'off'})", prediction.replace(" ", ""))


    def test_process(self):
        self.assistant.process("schalte die stehlampe aus")
        result = input("wurde die stehlampe angeschaltet ? y/n:")
        if result != "y":
            self.fail()

    def test_hue_app(self):
        self.assistant.apps.hue.setlights({"stehlampe": "on"})
        result = input("wurde die stehlampe angeschaltet ? y/n:")
        if result != "y":
            self.fail()

    def test_timer_app(self):
        self.assistant.apps.timer.set("00:00:01")
        result = input("haben sie einen Wecker klingeln gehört ?: y/n")
        if result != "y":
            self.fail()
              
    def test_speechCenter_say(self):
        #check if TTS.say() finishes in reasonable time
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)
        try:
            self.assistant.speechCent.say("test satz")
        except TimeoutError:
            self.fail("TTS.say() took too long to exceute")
            
        finally:
            signal.alarm(0)
