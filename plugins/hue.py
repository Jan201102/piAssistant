"""
Phillips Hue plugin
"""

from hue_api import HueApi
import tensorflow as tf
import logging
from time import sleep

class Plugin:
    def __init__(self, memory, **kwargs):
        self.memory = memory
        self.api = HueApi()
        self.model = tf.keras.models.load_model("./plugins/light_controll.h5",custom_objects={'Functional': tf.keras.models.Model})
        try:
            self.api.load_existing()
            self.lights = [light for light in self.api.fetch_lights()]
        except :
            if "ip" in kwargs.keys():
                ip = kwargs["ip"]
                print("please press the connect button on th huebridge")
            else:
                ip = input('press connect-button on huebridge and enter ip-address:')
            print("connecting")
            for _ in range(20):
                try:
                    self.api.create_new_user(ip)
                    self.api.save_api_key()
                    print("Done")
                    break
                except:
                    sleep(1)

        self.lights = [light for light in self.api.fetch_lights()]

    def process(self, command):
        data= {}
        splitCommand = list(command)
        tokenCommand = tf.keras.preprocessing.sequence.pad_sequences([[ord(char) for char in splitCommand]],maxlen=256)
        pred = self.model.predict(tokenCommand)
        if pred[0].argmax() != 0:
            for light in self.lights:
                if light.name.lower() in command.replace('ß','ss') or pred[0].argmax() == 2:
                    logging.debug("{}".format(light.name))
                    if pred[1] >= 1:
                        light.set_on()
                        light.set_brightness(int(pred[1])*25)
                        data["value"] = int(pred[1])
                    else:
                        light.set_off()
                        data["value"] = 0
        else:
            data["label"] = "none"

        if pred[0].argmax() == 2:
            data["label"] = "all"
        else:
            data["label"] = "specific"

        self.memory.memorize("hue", **data)
