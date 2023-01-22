"""
Phillips HUe pulgin with TFlite
"""
import tflite_runtime.interpreter as tflite
from hue_api import HueApi
import logging
from time import sleep
import numpy as np
import zahlwort2num as w2n
class Plugin():
    def __init__(self,memory,**kwargs):
        # initializing model
        self.interpreter = tflite.Interpreter(model_path="./plugins/light_controll.tflite")
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        print(self.output_details)

        # initializing hue

        self.memory = memory
        self.api = HueApi()
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
        # filter numbers
        dimValue = 0
        for word in command.split(" "):
            try:
                w2n.convert(word)
                dimValue = w2n.convert(word)
            except:
                pass
        #preprocessing
        data = {}
        splitCommand = list(command)
        zeros = np.zeros((1,256),np.int32)
        for i in range(len(splitCommand)):
            pos = 256-len(splitCommand)+i
            zeros[0][pos] = ord(splitCommand[i])
        tokenCommand = zeros
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
                        light.set_brightness(int(255*dimValue/100))
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

