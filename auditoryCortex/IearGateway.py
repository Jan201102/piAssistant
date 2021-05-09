import abc
from abc import ABC

class IearGateway(ABC):
    @abc.abstractmethod
    def start_audio(self,record, timeout, threading, verbose):
        pass
    @abc.abstractmethod
    def get_audio(self):
        pass
    @abc.abstractmethod
    def stop_audio(self,verbose):
        pass