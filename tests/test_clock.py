from unittest import TestCase
import context
from piassistant.app import timer
from time import sleep

class TestPlugin(TestCase):
    def setUp(self) -> None:
        self.clock = timer.App()

    def test_alarm(self):
        self.clock.alarm(1)
        sleep(5)
    def test_set(self):
        self.clock.set("00:00:01")
        sleep(5)
