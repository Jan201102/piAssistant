import subprocess
import logging
from Isignals import Isignals


class Signals(Isignals):
    def __init(self):
        self.lightName = "Regal/setRGBW"
        self.value = "000000ff"
        self.host= "192.168.2.107"

    def activate(self):
        logging.debug("lighting up Signal")
        subprocess.call("mqtt_pub -h {} -t {} -m {}".format(self.host, self.lightName, self.value), shell=True)

    def deactivate(self):
        logging.debug("turning off signal")
        subprocess.call("mqtt_pub -h {} -t {} -m {}".format(self.host, self.lightName, "00000000"), shell=True)
