"""
Phillips Hue plugin
"""

from hue_api import HueApi
from time import sleep
import tensorflow as tf
import logging


class Plugin:
    def __init__(self):
        self.api = HueApi()
        self.model = tf.keras.models.load_model("./plugins/light_controll.h5",custom_objects={'Functional': tf.keras.models.Model})
        try:
            self.api.load_existing()
            self.lights = [light for light in self.api.fetch_lights()]
        except :
            ip = input('press connect-button on huebridge and enter ip-address:')
            self.api.create_new_user(ip)
            self.api.save_api_key()

        self.lights = [light for light in self.api.fetch_lights()]

    def process(self, command):
        splitCommand = list(command)
        tokenCommand = tf.keras.preprocessing.sequence.pad_sequences([[ord(char) for char in splitCommand]],maxlen=256)
        pred = self.model.predict(tokenCommand)
        if pred[0].argmax() != 0:
            for light in self.lights:
                if light.name.lower() in command.replace('ß','ss') or pred[0].argmax() == 2:
                    logging.DEBUG("{}".format(light.name))
                    if pred[1] >= 1:
                        light.set_on()
                        light.set_brightness(int(pred[1])*25)
                    else:
                        light.set_off()
