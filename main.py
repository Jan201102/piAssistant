from auditoryCortex.AuditoryCortex import *
from speechCenter.speechCenter import *
import importlib
import json


class Main(AuditoryCortex, SpeechCenter):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.import_plugins = json.load(open("config/plugins.json"))
        self.plugins = []
        for import_plugin in self.import_plugins:
            plugin_module = importlib.import_module("plugins."+import_plugin, ".")
            plugin = plugin_module.Plugin()
            self.plugins.append(plugin)

    def process(self,text):
        print(text)
        for plugin in self.plugins:
            plugin.process(text)

    def start(self):
        while True:
            print('listening...')
            # print(a.listen(file='-1742047633.wav'))
            if self.wait():
                command = self.listen(record=True)
                print(command[0][0])
                self.process(command[0][0]['text'])
                """
                result_length = [len(lang['result']) for lang in command[0]]
                min = max(result_length)
                min_result = result_length.index(min)
                result = []
                partial_result = []

                for i, word in enumerate(command[0][min_result]['result']):
                    start = round(word['start'], 1)
                    end = round(word['end'], 1)
                    for lang in command[0]:
                        for word in lang['result']:
                            if round(word['start']) >= start - 0.1 and round(word['end'], 2) <= end + 0.1:
                                partial_result.append(word)
                    conf = 0
                    resulting_word = ''
                    print(partial_result)
                    for word in partial_result:
                        if word['conf'] > conf:
                            conf = word['conf']
                            resulting_word = word
                    result.append(word)
                    partial_result = []
                print(result)
                for word in result:
                    print(word['word'])
                """