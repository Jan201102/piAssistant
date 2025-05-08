import unittest
import context
from piassistant.app.weather import App


class TestWeatherSimple(unittest.TestCase):
    def setUp(self) -> None:
        location = "Stuttgart"
        self.weather = App( location=location)

    def test_request(self):
        answer  = self.weather.request("daily",when=1)
        print(answer)
