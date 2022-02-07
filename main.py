from auditoryCortex.auditoryCortex import *
from speechCenter.speechCenter import *
from memory.memory import Memory
from signals.signals import Signals
import importlib
import json
import logging

class Main:
    def __init__(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)
        self.memory = Memory()
        self.audiCort = AuditoryCortex(*args, **kwargs)
        self.speechCent = SpeechCenter()
        self.import_plugins = json.load(open("config/plugins.json"))
        self.plugins = []
        self.signals = Signals()
        for import_plugin in self.import_plugins:
            plugin_module = importlib.import_module("plugins."+import_plugin, ".")
            plugin = plugin_module.Plugin()
            self.plugins.append(plugin)

    def process(self, text):
        for plugin in self.plugins:
            plugin.process(text)

    def start(self):
        while True:
            logging.info('listening...')

            if self.audiCort.wait():
                self.signals.activate()
                command = self.audiCort.listen(record=True,verbose=0)
                logging.info(command)
                self.memory.memorize(command[1], command[0][0]['text'])
                self.process(command[0][0]['text'])
                self.signals.deactivate()
