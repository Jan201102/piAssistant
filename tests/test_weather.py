import unittest
import context
from piassistant.app.weather import App


class TestWeatherSimple(unittest.TestCase):
    def setUp(self) -> None:
        apiKey = ""
        location = ""
        self.weather = App(apiKey=apiKey, location=location)

    def test_request(self):
        self.weather.request("daily", type="rain")
