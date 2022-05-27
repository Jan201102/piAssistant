"""
Phillips HUe pulgin with TFlite
"""
import tensorflow as tf
from hue_api import HueApi
import logging
from time import sleep


class Plugin():
    def __init__(self,memory,**kwargs):
        # initializing model
        self.interpreter = tf.lite.Interpreter(model_path="./plugins/light_controll.tflite")
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        print(self.output_details)

        # initializing hue

        self.memory = memory
        self.api = HueApi()
        self.model = tf.keras.models.load_model("./plugins/light_controll.h5",
                                                custom_objects={'Functional': tf.keras.models.Model})
        try:
            self.api.load_existing()
            self.lights = [light for light in self.api.fetch_lights()]

        except:
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
                    print(".")
                    sleep(1)

        self.lights = [light for light in self.api.fetch_lights()]

    def process(self,command):
        #preprocessing
        data = {}
        splitCommand = list(command)
        tokenCommand = tf.keras.preprocessing.sequence.pad_sequences([[ord(char) for char in splitCommand]], maxlen=256)

        #model prediction
        self.interpreter.set_tensor(self.input_details[0]['index'], tokenCommand)
        self.interpreter.invoke()
        lightType = self.interpreter.get_tensor(self.output_details[1]['index']).argmax()
        brightness = self.interpreter.get_tensor(self.output_details[0]['index'])

        #switch lights
        if lightType != 0:
            for light in self.lights:
                if light.name.lower() in command.replace('ß','ss') or lightType == 2:
                    logging.debug("{}".format(light.name))
                    if brightness >= 1:
                        light.set_on()
                        light.set_brightness(int(brightness)*25)
                        data["value"] = int(brightness)
                    else:
                        light.set_off()
                        data["value"] = 0
        else:
            data["label"] = "none"

        if lightType == 2:
            data["label"] = "all"
        else:
            data["label"] = "specific"
        data["text"] = command
        self.memory.memorize("hue", **data)

