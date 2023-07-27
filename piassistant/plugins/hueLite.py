"""
Phillips HUe pulgin with TFlite
"""

import tflite_runtime.interpreter as tflite
from hue_api import HueApi
import logging
from time import sleep
import numpy as np
import json


class Plugin:
    def __init__(self, memory, **kwargs):
        # initializing model
        self.encoder = tflite.Interpreter("/content/drive/MyDrive/deeplearning/seq_to_Seq/Hue/hue_encoder_LSTM.tflite")
        self.decoder = tflite.Interpreter("/content/drive/MyDrive/deeplearning/seq_to_Seq/Hue/hue_decoder_LSTM.tflite")

        self.encoder.allocate_tensors()
        self.decoder.allocate_tensors()

        self.encoderInputDetails = self.encoder.get_input_details()
        self.decoderInputDetails = self.decoder.get_input_details()
        self.encoderOutputDetails = self.encoder.get_output_details()
        self.decoderOutputDetails = self.decoder.get_output_details()

        with open("/content/drive/MyDrive/deeplearning/seq_to_Seq/Hue/hue_tokenizer.json", "r") as f:
            all = json.loads(f.read())
            self.vocab = json.loads(all["config"]["word_index"])

        with open("/content/drive/MyDrive/deeplearning/seq_to_Seq/Hue/hue_cmdtokenizer.json", "r") as f:
            all = json.loads(f.read())
            self.cmdWordIndex = json.loads(all["config"]["word_index"])
            self.cmdIndexWord = json.loads(all["config"]["index_word"], parse_int=True)

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

    def vectorizeInput(self, sentence, length):
        x = np.zeros(shape=(1, length), dtype=np.float32)
        words = sentence.split()
        for i, word in enumerate(words):
            if word in self.vocab.keys():
                x[0][i] = int(self.vocab[word])
        return x

    def predictCorrect(self, text, encoder, decoder):
        input = self.vectorizeInput(text, 50)
        encoder.set_tensor(self.encoderInputDetails[0]['index'], input)
        encoder.invoke()
        sequences = encoder.get_tensor(self.encoderOutputDetails[2]['index'])
        h = encoder.get_tensor(self.encoderOutputDetails[1]['index'])
        c = encoder.get_tensor(self.encoderOutputDetails[0]['index'])

        decoder_seq = np.zeros((1, 1), dtype="float32")
        decoder_seq[0, 0] = np.float32(self.cmdWordIndex["<start>"])
        plain_text = ""
        for i in range(50):
            decoder.set_tensor(self.decoderInputDetails[1]['index'], sequences)
            decoder.set_tensor(self.decoderInputDetails[0]['index'], h)
            decoder.set_tensor(self.decoderInputDetails[3]['index'], c)
            decoder.set_tensor(self.decoderInputDetails[2]['index'], decoder_seq)

            decoder.invoke()

            char_index = np.argmax(decoder.get_tensor(self.decoderOutputDetails[3]['index'])[0, -1, :])
            h = decoder.get_tensor(self.decoderOutputDetails[2]['index'])
            c = decoder.get_tensor(self.decoderOutputDetails[1]['index'])

            if char_index == 0:
                return plain_text
            plain_text += " " + self.cmdIndexWord[str(char_index)]

            decoder_seq = np.zeros((1, 1), dtype="float32")
            decoder_seq[0, 0] = char_index

    def output_to_json(self, output):
        logging.debug("Converting result to Json...")
        try:
            jsonS = '{'
            if output != "None":
                cmd = output.split()
                for word in cmd:
                    if word == ":":
                        jsonS += " : "
                    elif word == ",":
                        jsonS += " , "
                    elif word.isnumeric():
                        jsonS += word
                    else:
                        jsonS += '"' + word + '"'
            jsonS += "}"
            js = json.loads(jsonS)
            logging.debug("Done")
        except:
            js = json.loads("{}")
            logging.debug("Model generated no valid result")

        return js

    def setLight(self, light, action):
        logging.debug("setting light {}".format(light.name))
        if action == "on":
            light.set_on()
        elif action == "off":
            light.set_off()
        else:
            light.set_brightness(int(action * 255 / 100))

    def process(self, command):
        logging.debug("running Hue-Inference...")
        modelOutput = self.predictCorrect(command, self.encoder, self.decoder)
        logging.debug("Done")
        jsonquery = self.output_to_json(modelOutput)
        # switch lights
        for lightcommand in jsonquery.items():
            if lightcommand[0] == "all" or lightcommand[0] == " ":
                for light in self.lights:
                    self.setLight(light, lightcommand[1])
            else:
                for light in self.lights:
                    if light.name.lower() == lightcommand[0]:
                        self.setLight(light, lightcommand[1])
        data = {"command": command, "result": modelOutput}
        self.memory.memorize("hue", **data)
