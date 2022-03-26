import subprocess
import logging
from signals.Isignals import Isignals


class Signals(Isignals):
    def __init__(self,**config):
        if "host" in config.keys():
            self.host = config["host"]
        else:
            self.host = "192.168.2.107"
        if "light" in config.keys():
            self.lightName = config["light"]
        else:
            self.lightName = "Regal/setRGBW"
        self.value = "000000ff"


    def activate(self):
        logging.debug("lighting up Signal")
        try:
            subprocess.call("mosquitto_pub -h {} -t {} -m {}".format(self.host, self.lightName, self.value), shell=True)
        except:
            logging.warning("mqtt command failed")

    def deactivate(self):
        logging.debug("turning off signal")
        try:
            subprocess.call("mosquitto_pub -h {} -t {} -m {}".format(self.host, self.lightName, "00000000"), shell=True)
        except:
            logging.warning("mqtt command failed")
