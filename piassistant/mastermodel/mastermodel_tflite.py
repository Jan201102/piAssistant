from piassistant.Imastermodel import Imastermodel
import tflite_runtime.interpreter as tflite
from os import path
import json
import numpy as np

class Mastermodel(Imastermodel):

    def __init__(self):
        self.templateFolder = path.join(path.dirname(__file__), "./templates")
        self.encoder = tflite.Interpreter(path.join(self.templateFolder, "mastermodel_decoder_LSTM_64_V0_3.tflite"))
        self.decoder = tflite.Interpreter(path.join(self.templateFolder, "mastermodel_decoder_LSTM_64_V0_3.tflite"))

        self.encoder.allocate_tensors()
        self.decoder.allocate_tensors()

        self.encoderInputDetails = self.encoder.get_input_details()
        self.decoderInputDetails = self.decoder.get_input_details()
        self.encoderOutputDetails = self.encoder.get_output_details()
        self.decoderOutputDetails = self.decoder.get_output_details()

        with open(path.join(self.templateFolder, "mastermodel_tokenizer_64_V0_3.json"), "r") as f:
            all = json.loads(f.read())
            self.vocab = json.loads(all["config"]["word_index"])

        with open(path.join(self.templateFolder, "mastermodel_cmdtokenizer_64_V0_3.json"), "r") as f:
            all = json.loads(f.read())
            self.cmdWordIndex = json.loads(all["config"]["word_index"])
            self.cmdIndexWord = json.loads(all["config"]["index_word"], parse_int=True)

    def vectorizeInput(self, sentence, length):
        x = np.zeros(shape=(1, length), dtype=np.float32)
        words = sentence.split()
        for i, word in enumerate(words):
            if word in self.vocab.keys():
                x[0][i] = int(self.vocab[word])
        return x

    def run_mastermodel(self, text, len_seq=50):
        input = self.vectorizeInput(text, 50)
        self.encoder.set_tensor(self.encoderInputDetails[0]['index'], input)
        self.encoder.invoke()
        sequences = self.encoder.get_tensor(self.encoderOutputDetails[2]['index'])
        h = self.encoder.get_tensor(self.encoderOutputDetails[1]['index'])
        c = self.encoder.get_tensor(self.encoderOutputDetails[0]['index'])

        decoder_seq = np.zeros((1, 1), dtype="float32")
        decoder_seq[0, 0] = np.float32(self.cmdWordIndex["<start>"])
        plain_text = ""
        for i in range(50):
            self.decoder.set_tensor(self.decoderInputDetails[1]['index'], sequences)
            self.decoder.set_tensor(self.decoderInputDetails[0]['index'], h)
            self.decoder.set_tensor(self.decoderInputDetails[3]['index'], c)
            self.decoder.set_tensor(self.decoderInputDetails[2]['index'], decoder_seq)

            self.decoder.invoke()

            char_index = np.argmax(decoder.get_tensor(self.decoderOutputDetails[3]['index'])[0, -1, :])
            h = self.decoder.get_tensor(self.decoderOutputDetails[2]['index'])
            c = self.decoder.get_tensor(self.decoderOutputDetails[1]['index'])

            if char_index == 0:
                return plain_text
            plain_text += " " + self.cmdIndexWord[str(char_index)]

            decoder_seq = np.zeros((1, 1), dtype="float32")
            decoder_seq[0, 0] = char_index
