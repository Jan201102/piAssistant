import abc

class IauditoryCortexGateway(abc.ABC):
    @abc.abstractmethod
    def __init__(self,models,kws_model,name):
        pass
    @abc.abstractmethod
    def listen(self,file: str, record: bool ,verbose: bool) -> [{},str]:
        '''
        :param file: name of a file, that shold be transcribed
        :param record: True if your speech should be saved to an wave file
        :param verbose: True if you want commandline output
        :return: returns a list [{'text':str},filename], the field 'text' is what your assistant understood,
                                                         filename is the name of the audio file if record was True.
        '''
        pass
    @abc.abstractmethod
    def wait(self):
        pass
