from unittest import TestCase
from piassistant.plugins import clock

class TestPlugin(TestCase):
    def setUp(self) -> None:
        self.clock = clock.Plugin()

    def test_alarm(self):
        self.clock.alarm(0.1)
