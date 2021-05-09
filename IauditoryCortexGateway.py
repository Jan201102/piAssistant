import abc
from abc import ABC

class IauditoryCortexGateway(ABC):
    @abc.abstractmethod
    def __init__(self,models,kws_model,name):
        pass
    @abc.abstractmethod
    def listen(self,record,verbose):
        pass
    @abc.abstractmethod
    def wait(self):
        pass
