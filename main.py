from auditoryCortex.auditoryCortex import *
from speechCenter.speechCenter import *
from memory.memory import Memory
from signals.signals import Signals
import importlib
import json
import logging
import json

class Main:
    def __init__(self, *args, **kwargs):
        logging.basicConfig(format= "%(asctime)6s %(message)s",level=logging.INFO)
        logging.info("Starting Assistant...")
        with open(kwargs["configFile"],"r") as file:
            config = json.load(file)

        self.memory = Memory()
        self.audiCort = AuditoryCortex(*args,**config["assistant"])
        self.speechCent = SpeechCenter()
        self.signals = Signals()

        self.import_plugins = config["plugins"].keys()
        self.plugins = []

        for import_plugin in self.import_plugins:
            plugin_module = importlib.import_module("plugins."+import_plugin, ".")
            plugin = plugin_module.Plugin(self.memory, **config["plugins"][import_plugin])
            self.plugins.append(plugin)

        logging.info("Assistant ready")

    def process(self, text):
        for plugin in self.plugins:
            result = plugin.process(text)
            if result is not None:
                self.speechCent.say(result)


    def start(self):
        while True:
            logging.info('listening...')

            if self.audiCort.wait():
                logging.info("Key word detected")
                self.signals.activate()
                command = self.audiCort.listen(record=True,verbose=0)
                logging.info("understood: " + command[0][0]["text"])
                self.process(command[0][0]['text'])
                self.memory.memorize_audio(command[1], command[0][0]['text'])
                self.signals.deactivate()
