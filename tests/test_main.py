import unittest
from piassistant.main import Main
import logging

class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.assistant = Main(configFile="C:/Users/Jan_L/PycharmProjects/piAssistant1/piassistant/templates/config.json")

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

