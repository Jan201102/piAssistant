"""
Phillips Hue plugin
"""

from hue_api import HueApi
from time import sleep


class Plugin:
    def __init__(self):
        self.api = HueApi()
        try:
            self.api.load_existing()
            self.lights = [light for light in self.api.fetch_lights()]
        except :
            ip = input('press connect-button on huebridge and enter ip-address:')
            self.api.create_new_user(ip)
            self.api.save_api_key()

        self.lights = [light for light in self.api.fetch_lights()]

    def process(self, command):
        for light in self.lights:
            if light.name.lower() in command.replace('ß','ss'):
                if 'an' in command:
                    light.set_on()
                if 'aus' in command:
                    light.set_off()
                if 'heller' in command:
                    light.set_brightness(255)
                if 'dunkler' in command:
                    light.set_brightness(125)

