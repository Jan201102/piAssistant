"""
Phillips Hue plugin
"""

from hue_api import HueApi
import tensorflow as tf
import numpy as np
import json
import logging
from time import sleep
import zahlwort2num as w2n

class Plugin:
    def __init__(self, memory, **kwargs):
        self.memory = memory
        self.api = HueApi()
        with open("./plugins/hue_cmdtokenizer.json","r") as f:
            self.cmdTokenizer = tf.keras.preprocessing.text.tokenizer_from_json(f.read())
        with open("./plugins/hue_tokenizer.json","r") as f:
            self.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(f.read())
        self.encoder =  tf.keras.models.load_model("./plugins/hue_encoder.h5")
        self.decoder =  tf.keras.models.load_model("./plugins/hue_decoder.h5",custom_objects={"AttentionLayer":AttentionLayer})

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
    def predict_correct(self,text, encoder, decoder, text_tokenizer, cmd_tokenizer, len_seq=50):
        x = text_tokenizer.texts_to_sequences([text])
        x = tf.keras.utils.pad_sequences(x, 50, padding='post', truncating='post')
        sequences, state = encoder.predict(x)

        decoder_seq = np.zeros((1, 1))
        decoder_seq[0, 0] = cmd_tokenizer.word_index['<start>']
        attn = []
        plain_text = ""
        for i in range(len_seq):
            output_char, attention, dec_state = decoder.predict(
                [sequences, state, decoder_seq])
            char_index = np.argmax(output_char[0, -1, :])
            if char_index == 0:
                return plain_text
            plain_text += " " + cmd_tokenizer.index_word[char_index]
            print(plain_text)

            decoder_seq = np.zeros((1, 1))
            decoder_seq[0, 0] = char_index
            state = dec_state
            attn.append(attention)

        return plain_text

    def output_to_json(self,output):
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
        except:
            js = json.loads("{}")
            logging.debug("Model generated no valid result")

        return js

    def setLight(self,light,action):
        if action == "on":
            light.set_on()
        elif action == "off":
            light.set_off()
        else:
            light.set_brightness(int(action*255/100))
    def process(self, command):
        modelOutput = self.predict_correct(command,self.encoder,self.decoder,self.tokenizer,self.cmdTokenizer)
        jsonquery = self.output_to_json(modelOutput)
        for lightcommand in jsonquery.items():
            if lightcommand[0] == "all":
                for light in self.lights:
                    self.setLight(light,lightcommand[1])
            else:
                for light in self.lights:
                    if light.name.lower() == lightcommand[0]:
                        self.setLight(light,lightcommand[1])
        data ={"command":command,"result":modelOutput}
        self.memory.memorize("hue",**data)

from keras.layers import Layer
from keras import backend as K


class AttentionLayer(Layer):
    """
    Attention Layer von Thushan Ganegedara,
    verfügbar unter https://github.com/thushv89/attention_keras

    This class implements Bahdanau attention (https://arxiv.org/pdf/1409.0473.pdf).
    There are three sets of weights introduced W_a, U_a, and V_a
     """

    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        assert isinstance(input_shape, list)
        # Create a trainable weight variable for this layer.

        self.W_a = self.add_weight(name='W_a',
                                   shape=tf.TensorShape((input_shape[0][2], input_shape[0][2])),
                                   initializer='uniform',
                                   trainable=True)
        self.U_a = self.add_weight(name='U_a',
                                   shape=tf.TensorShape((input_shape[1][2], input_shape[0][2])),
                                   initializer='uniform',
                                   trainable=True)
        self.V_a = self.add_weight(name='V_a',
                                   shape=tf.TensorShape((input_shape[0][2], 1)),
                                   initializer='uniform',
                                   trainable=True)

        super(AttentionLayer, self).build(input_shape)  # Be sure to call this at the end

    def call(self, inputs, verbose=False):
        """
        inputs: [encoder_output_sequence, decoder_output_sequence]
        """
        assert type(inputs) == list
        encoder_out_seq, decoder_out_seq = inputs
        if verbose:
            print('encoder_out_seq>', encoder_out_seq.shape)
            print('decoder_out_seq>', decoder_out_seq.shape)

        def energy_step(inputs, states):
            """ Step function for computing energy for a single decoder state """

            assert_msg = "States must be a list. However states {} is of type {}".format(states, type(states))
            assert isinstance(states, list) or isinstance(states, tuple), assert_msg

            """ Some parameters required for shaping tensors"""
            en_seq_len, en_hidden = encoder_out_seq.shape[1], encoder_out_seq.shape[2]
            de_hidden = inputs.shape[-1]

            """ Computing S.Wa where S=[s0, s1, ..., si]"""
            # <= batch_size*en_seq_len, latent_dim
            reshaped_enc_outputs = K.reshape(encoder_out_seq, (-1, en_hidden))
            # <= batch_size*en_seq_len, latent_dim
            W_a_dot_s = K.reshape(K.dot(reshaped_enc_outputs, self.W_a), (-1, en_seq_len, en_hidden))
            if verbose:
                print('wa.s>', W_a_dot_s.shape)

            """ Computing hj.Ua """
            U_a_dot_h = K.expand_dims(K.dot(inputs, self.U_a), 1)  # <= batch_size, 1, latent_dim
            if verbose:
                print('Ua.h>', U_a_dot_h.shape)

            """ tanh(S.Wa + hj.Ua) """
            # <= batch_size*en_seq_len, latent_dim
            reshaped_Ws_plus_Uh = K.tanh(K.reshape(W_a_dot_s + U_a_dot_h, (-1, en_hidden)))
            if verbose:
                print('Ws+Uh>', reshaped_Ws_plus_Uh.shape)

            """ softmax(va.tanh(S.Wa + hj.Ua)) """
            # <= batch_size, en_seq_len
            e_i = K.reshape(K.dot(reshaped_Ws_plus_Uh, self.V_a), (-1, en_seq_len))
            # <= batch_size, en_seq_len
            e_i = K.softmax(e_i)

            if verbose:
                print('ei>', e_i.shape)

            return e_i, [e_i]

        def context_step(inputs, states):
            """ Step function for computing ci using ei """
            # <= batch_size, hidden_size
            c_i = K.sum(encoder_out_seq * K.expand_dims(inputs, -1), axis=1)
            if verbose:
                print('ci>', c_i.shape)
            return c_i, [c_i]

        def create_inital_state(inputs, hidden_size):
            # We are not using initial states, but need to pass something to K.rnn funciton
            fake_state = K.zeros_like(inputs)  # <= (batch_size, enc_seq_len, latent_dim
            fake_state = K.sum(fake_state, axis=[1, 2])  # <= (batch_size)
            fake_state = K.expand_dims(fake_state)  # <= (batch_size, 1)
            fake_state = K.tile(fake_state, [1, hidden_size])  # <= (batch_size, latent_dim
            return fake_state

        fake_state_c = create_inital_state(encoder_out_seq, encoder_out_seq.shape[-1])
        fake_state_e = create_inital_state(encoder_out_seq,
                                           encoder_out_seq.shape[1])  # <= (batch_size, enc_seq_len, latent_dim

        """ Computing energy outputs """
        # e_outputs => (batch_size, de_seq_len, en_seq_len)
        last_out, e_outputs, _ = K.rnn(
            energy_step, decoder_out_seq, [fake_state_e],
        )

        """ Computing context vectors """
        last_out, c_outputs, _ = K.rnn(
            context_step, e_outputs, [fake_state_c],
        )

        return c_outputs, e_outputs

    def compute_output_shape(self, input_shape):
        """ Outputs produced by the layer """
        return [
            tf.TensorShape((input_shape[1][0], input_shape[1][1], input_shape[1][2])),
            tf.TensorShape((input_shape[1][0], input_shape[1][1], input_shape[0][1]))
        ]