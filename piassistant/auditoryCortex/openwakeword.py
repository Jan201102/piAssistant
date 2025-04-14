import logging
from openwakeword.model import Model
import numpy as np


class OpenWakeWordDetector:
    def __init__(self, ear,openwakewordmodels, **kwargs):
        logging.info("initializing openwakeword detector")
        self.ear = ear
        self.model = Model(wakeword_models=openwakewordmodels)
        logging.info("Done")

    def wait(self):
        self.ear.start_audio(threading=False)
        self.model.reset()
        while True:
            self.model.predict(np.frombuffer(self.ear.get_audio(),dtype=np.int16))

            for mdl in self.model.prediction_buffer.keys():
                #get all scores for the model
                scores = list(self.model.prediction_buffer[mdl])
                if scores[-1] > 0.5:
                    self.ear.stop_audio()

                    return True

