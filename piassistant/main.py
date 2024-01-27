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
        logging.basicConfig(format="%(asctime)6s %(message)s",handlers=[logging.FileHandler("piassistant.log"),logging.StreamHandler()], level=logging.DEBUG)
        logging.info("Starting Assistant...")
        with open(kwargs["configFile"], "r") as file:
            config = json.load(file)

        self.signals = Signals(**config["assistant"])
        self.memory = Memory()
        self.audiCort = AuditoryCortex(*args, **config["assistant"])
        self.signals.showStartup(10)
        self.speechCent = SpeechCenter()
        self.signals.showStartup(30)
        
        # load mastermodel
        backend = "tensorflow"
        for pkg in pkgutil.iter_modules():
            if pkg.name == "tensorflow":
                backend = "tensorflow"
                break
            if pkg.name == "tflite_runtime":
                backend = "tflite"

        if backend == "tensorflow":
            mastermodel_class = importlib.import_module("piassistant.mastermodel.mastermodel",".")
        elif backend == "tflite":
            mastermodel_class = importlib.import_module("piassistant.mastermodel.mastermodel_tflite",".")

        self.mastermodel = mastermodel_class.Mastermodel()
        self.signals.showStartup(50)

        # load plugins
        self.import_plugins = config["plugins"].keys()
        self.plugins = []
        logging.info("loading plugins...")
        for import_plugin in self.import_plugins:
            plugin_module = importlib.import_module("plugins." + import_plugin, ".")
            plugin = plugin_module.Plugin(self.memory, **config["plugins"][import_plugin])
            self.plugins.append(plugin)
        logging.info("plugins loaded.")
        self.signals.showStartup(70)
        
        # load apps
        logging.info("load apps...")
        self.apps = AppHandler(**config["apps"])
        logging.info("apps loaded.")
        self.signals.showStartup(90)
        
        self.signals.showStartupSuccess()
        logging.info("Assistant ready")

    def process(self, text):
        result = None
        action = self.mastermodel.run_mastermodel(text).strip()
        logging.debug(f"mastermodel produced command {action}")
        if action != "none":
            action = "self.apps." + action
            try:
                result = eval(action)
            except (SyntaxError,AttributeError) as error:
                result = None
                logging.error(f'model produced invalid python command: {action}')
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
                self.signals.showProcessing()
                self.process(command[0][0]['text'])
                self.memory.memorize_audio(command[1], command[0][0]['text'])
                self.signals.deactivate()

