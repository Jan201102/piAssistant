"""
Phillips Hue plugin
"""

from hue_api import HueApi
import logging
from time import sleep


class App:
    def __init__(self, **kwargs):
        self.api = HueApi()
        try:
            self.api.load_existing()
            self.lights = [light for light in self.api.fetch_lights()]
        except:
            if "ip" in kwargs.keys():
                ip = kwargs["ip"]
                print("please press the connect button on th huebridge")
            else:
                ip = input('press connect-button on huebridge and enter ip-address:')
            print("connecting...")
            for _ in range(20):
                try:
                    self.api.create_new_user(ip)
                    self.api.save_api_key()
                    print("Done")
                    break
                except KeyboardInterrupt:
                    raise(KeyboardInterrupt)
                except:
                    sleep(1)

        self.lights = [light for light in self.api.fetch_lights()]

    @staticmethod
    def set_light(light, action):
        logging.debug("setting light {}".format(light.name))
        if type(action) == str:
            action = action.strip()
            if action == "on":
                light.set_on()
            elif action == "off":
                light.set_off()
        else:
            light.set_on()
            light.set_brightness(int(action * 255 / 100))

    def setlights(self, lights: dict):
        for lightcommand in lights.items():
            if lightcommand[0].strip() == "all":
                for light in self.lights:
                    self.set_light(light, lightcommand[1])
            else:
                for light in self.lights:
                    if light.name.lower() == lightcommand[0].strip().lower():
                        self.set_light(light, lightcommand[1])
