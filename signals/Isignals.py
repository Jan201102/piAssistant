import abc
from abc import ABC


class Isignals(ABC):

    @abc.abstractmethod
    def __init__(self):
        """
        Currently does nothing, may be used to initialize external device connections, etc.
        :return: None
        """
        pass

    def activate(self):
        """
        lights up a light or something else to show the user it recognized the wish of interaction
        :return: None
        """
        pass

    def deactivate(self):
        """
        reverses the action executed by activate(self), to show the assistant waits for interaction
        :return: None
        """
        pass
