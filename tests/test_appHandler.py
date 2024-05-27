import unittest
import context
from piassistant.app.appHandler import AppHandler


class TestAppHandler(unittest.TestCase):
    def test(self):
        AppHandler(**{"hue":{"ip":"192.168.2.106"}})