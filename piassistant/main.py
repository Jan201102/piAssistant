import logging
logging.basicConfig(format="%(asctime)6s %(message)s",handlers=[logging.FileHandler("piassistant.log"),logging.StreamHandler()], level=logging.DEBUG)
from piassistant.auditoryCortex.auditoryCortex import *
from piassistant.speechCenter.speechCenter import SpeechCenter
from piassistant.memory.memory import Memory
from piassistant.signals.signals import Signals
from piassistant.app.appHandler import AppHandler
import importlib

import json
import pkgutil
import platform


class Main:
    def __init__(self, *args, **kwargs):
        print("starting assistant...")
        logging.basicConfig(format="%(asctime)6s %(message)s",handlers=[logging.FileHandler("piassistant.log"),logging.StreamHandler()], level=logging.DEBUG)
        logging.info("Starting Assistant...")
        with open(kwargs["configFile"], "r") as file:
            config = json.load(file)

        self.signals = Signals(**config["assistant"])
        self.memory = Memory()
        self.audiCort = AuditoryCortex(*args, **config["assistant"])
        self.signals.showStartup(10)
        self.speechCent = SpeechCenter(**config["assistant"])
        self.AudioOutput = SpeakerHandler()
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
        
        logging.debug("processed user input")
        if result is not None:
            logging.debug("calling speechCenter")
            self.speechCent.say(result)
        

    def start(self):
        while True:
            logging.info('listening...')
            if self.audiCort.wait():
                self.AudioOutput.mute_speakers()
                logging.info("Key word detected")
                self.signals.activate()
                command = self.audiCort.listen(record=True, verbose=False)
                logging.info("understood: " + command[0][0]["text"])
                self.signals.showProcessing()
                self.AudioOutput.unmute_speakers()
                self.process(command[0][0]['text'])
                self.memory.memorize_audio(command[1], command[0][0]['text'])
                self.signals.deactivate()
    
class SpeakerHandler():
    def __init__(self, *args, **kwargs):
        self.platform = platform.system()
        if self.platform == "Linux":
            self.mixer = self.init_linux()
        elif self.platform == "Windows":
            self.mixer = self.init_windows()
        self.volume = 50

    def init_linux(self):
        import alsaaudio
        available_cards = alsaaudio.cards()
        mixer = None
        
        # Try to find a suitable mixer control
        for card_idx, card in enumerate(available_cards):
            try:
                if card == "seeed2micvoicec" or "wm8960" in card:
                    mixer = alsaaudio.Mixer("Playback", cardindex=card_idx)
                    break
                elif card == "Headphones":
                    mixer = alsaaudio.Mixer("PCM", cardindex=card_idx)
                    break
            except alsaaudio.ALSAAudioError:
                continue
        
        # If no specific card found, try common mixer controls
        if mixer is None:
            common_controls = ["Master", "PCM", "Speaker", "Headphone", "Digital"]
            for control in common_controls:
                try:
                    mixer = alsaaudio.Mixer(control)
                    logging.info(f"Using mixer control: {control}")
                    break
                except alsaaudio.ALSAAudioError:
                    continue
        
        # If still no mixer found, list available controls and use the first one
        if mixer is None:
            try:
                mixers = alsaaudio.mixers()
                if mixers:
                    mixer = alsaaudio.Mixer(mixers[0])
                    logging.info(f"Using first available mixer control: {mixers[0]}")
                else:
                    logging.warning("No mixer controls found")
                    return None
            except alsaaudio.ALSAAudioError as e:
                logging.error(f"Failed to initialize any mixer: {e}")
                return None
        
        return mixer
    
    def init_windows(self):
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        return volume
    
    def mute_speakers(self):
        if self.mixer is None:
            logging.warning("Audio mixer not available - cannot mute speakers")
            return
            
        if self.platform == "Linux":
            self.volume = self.mixer.getvolume()[0]
            self.mixer.setvolume(0)
        elif self.platform == "Windows":
            self.mixer.SetMute(1, None)

    def unmute_speakers(self):
        if self.mixer is None:
            logging.warning("Audio mixer not available - cannot unmute speakers")
            return
            
        if self.platform == "Linux":
            self.mixer.setvolume(self.volume)
        elif self.platform == "Windows":
            self.mixer.SetMute(0, None)





