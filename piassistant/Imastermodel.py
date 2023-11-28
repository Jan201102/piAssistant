import abc

class Imastermodel(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def run_mastermodel(self, text: str, len_seq=50):
        """
        :param text: text the model should convert to a command
        :param len_seq: maximum number of words from text the modell uses for prediction
        :return: a python command, based on the text input
        """
        pass
