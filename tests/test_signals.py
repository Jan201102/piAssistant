import context
import unittest
from piassistant.signals.signals import Signals
import time


class TestSignals(unittest.TestCase):
    def setUp(self):
        self.signals = Signals()
        self.addCleanup(self.cleanup)

    def cleanup(self):
        del self.signals

    def test_show_startup(self):
        self.signals.showStartup(50)
        time.sleep(1)
        print("Startup displayed")

    def test_show_startup_success(self):
        self.signals.showStartupSuccess()
        time.sleep(1)
        print("Startup success displayed")

    def test_activate(self):
        self.signals.activate()
        time.sleep(1)
        print("Activated")

    def test_show_processing(self):
        self.signals.showProcessing()
        time.sleep(1)
        print("Processing displayed")

    def test_deactivate(self):
        self.signals.deactivate()
        time.sleep(1)
        print("Deactivated")


if __name__ == "__main__":
    unittest.main()