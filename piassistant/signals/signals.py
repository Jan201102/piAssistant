import logging
from .Isignals import Isignals

try:
    import RPi.GPIO as gpio
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as gpio


class Signals(Isignals):
    def __init__(self, **config):
        self.g = 40
        self.b = 38
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.g, gpio.OUT)
        gpio.setup(self.b, gpio.OUT)
        gpio.setwarnings(False)
        gpio.output(self.b, False)
        gpio.output(self.g, False)

    def activate(self):
        logging.debug("light up LED")
        gpio.output(self.b, True)
        gpio.output(self.g, True)

    def deactivate(self):
        logging.debug("LED off")
        gpio.output(self.b, False)
        gpio.output(self.g, False)
