from auditoryCortex.auditoryCortex import *
from speechCenter.speechCenter import *
import importlib
import json


class Main:
    def __init__(self, *args, **kwargs):
        self.audiCort = AuditoryCortex(*args, **kwargs)
        self.speechCent = SpeechCenter()
        self.import_plugins = json.load(open("config/plugins.json"))
        self.plugins = []
        for import_plugin in self.import_plugins:
            plugin_module = importlib.import_module("plugins."+import_plugin, ".")
            plugin = plugin_module.Plugin()
            self.plugins.append(plugin)

    def process(self, text):
        print(text)
        for plugin in self.plugins:
            plugin.process(text)

    def start(self):
        while True:
            print('listening...')

            if self.audiCort.wait():
                command = self.audiCort.listen()
                print(command[0][0])
                self.process(command[0][0]['text'])
