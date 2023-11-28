from piassistant.auditoryCortex.auditoryCortex import *
from piassistant.speechCenter.speechCenter import *
from piassistant.memory.memory import Memory
from piassistant.signals.signals import Signals
from piassistant.app.appHandler import AppHandler
import importlib
import logging
import json
import pkgutil


class Main:
    def __init__(self, *args, **kwargs):
        logging.basicConfig(format="%(asctime)6s %(message)s", level=logging.DEBUG)
        logging.info("Starting Assistant...")
        with open(kwargs["configFile"], "r") as file:
            config = json.load(file)

        self.memory = Memory()
        self.audiCort = AuditoryCortex(*args, **config["assistant"])
        self.speechCent = SpeechCenter()
        self.signals = Signals()

        # load mastermodel
        backend = "tensorflow"
        for pkg in pkgutil.iter_modules():
            if pkg.name == "tensorflow":
                backend = "tensorflow"
                break
            if pkg.name == "tflite_runtime":
                backend = "tflite"

        if backend == "tensorflow":
            mastermodel_class = importlib.import_module("mastermodel.mastermodel",".")
        elif backend == "tflite":
            mastermodel_class = importlib.import_module("mastermodel.mastermodel_tflite",".")

        self.mastermodel = mastermodel_class.Mastermodel()


        # load plugins
        self.import_plugins = config["plugins"].keys()
        self.plugins = []
        logging.info("loading plugins...")
        for import_plugin in self.import_plugins:
            plugin_module = importlib.import_module("plugins." + import_plugin, ".")
            plugin = plugin_module.Plugin(self.memory, **config["plugins"][import_plugin])
            self.plugins.append(plugin)
        logging.info("plugins loaded.")

        # load apps
        logging.info("load apps...")
        self.apps = AppHandler(**config["apps"])
        logging.info("apps loaded.")

        logging.info("Assistant ready")

    def process(self, text):
        result = None
        action = self.mastermodel.run_mastermodel(text)
        logging.debug(action)
        if action != "none":
            action = "self.apps." + action
            try:
                result = eval(action)
            except SyntaxError:
                result = None
                logging.error("model produced invalid python command")
        else:
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
                command = self.audiCort.listen(record=True, verbose=False)
                logging.info("understood: " + command[0][0]["text"])
                self.process(command[0][0]['text'])
                self.memory.memorize_audio(command[1], command[0][0]['text'])
                self.signals.deactivate()

