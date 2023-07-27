import abc


class IauditoryCortexGateway(abc.ABC):
    @abc.abstractmethod
    def __init__(self, models, kws_model, name):
        pass

    @abc.abstractmethod
    def listen(self, file: str, timeout: int, verbose: bool) -> [{},str]:
        """
        :param file: name of a file, that should be transcribed
        :param timeout: max. length in seconds until the method stops the audio stream
        :param verbose: True if you want commandline output
        :return: returns a list [{'text':str},filename], the field 'text' is what your assistant understood,
        """
        pass

    @abc.abstractmethod
    def wait(self) -> bool:
        """
        This method runs, until the name of the assistant was detected
        :return: True, if the name was detected
        """
        pass
