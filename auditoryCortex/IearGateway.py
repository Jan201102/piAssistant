import abc
from abc import ABC


class IearGateway(ABC):

    @abc.abstractmethod
    def start_audio(self, timeout, verbose, file) -> None:
        """
        start an audio stream, read chunks with get_audio()
        :param file: audio file that should be decoded(optional)
        :param timeout: max. length in seconds until the method stops the audio stream
        :param verbose: True, vor detailed output
        :return: None
        """
        pass

    @abc.abstractmethod
    def get_audio(self):
        pass

    @abc.abstractmethod
    def stop_audio(self, verbose) -> None:
        """
        stop audio stream, which was started by start_audio()
        :param verbose: True, for detailed output
        :return: None
        """
        pass

