"""
homebridge plugin
"""
import json
import subprocess
import logging


class Plugin:
    def __init__(self):
        self.bulbs = json.load(open("config/homebridge.json"))["accessories"]
        self.colors = json.load(open("config/colors.json"))

    def process(self,text):
        light_type = "RGB"
        for lamp in self.bulbs:
            logging.debug(lamp)
            if lamp['accessory'] == 'mqttthing':
                topic = None
                value = None
                if lamp['type'] == "lightbulb" :
                    if lamp["name"].lower() in text or 'licht' in text or 'alle' in text:
                        if 'an' in text:
                            topic = lamp["topics"]["setOn"]
                            value = 'true'
                        if 'aus' in text:
                            topic = lamp["topics"]["setOn"]
                            value = 'false'

                        for color in self.colors.keys():
                            if color in text:
                                logging.debug('found color {}'.format(color))
                                if 'setRGBW' in lamp["topics"]:
                                    topic = lamp["topics"]["setRGBW"]
                                    light_type = "RGBW"
                                else:
                                    topic = lamp["topics"]["setRGB"]
                                    light_type= "RGB"
                                if color == 'weiß':
                                    if 'warm' in text:
                                        value = self.colors[color]['warm'][light_type]
                                    else:
                                        value = self.colors[color]['kalt'][light_type]
                                else:
                                    value = self.colors[color][light_type]
                if topic != None and value != None:
                    logging.info('setting {} to {}'.format(topic, value))
                    subprocess.call('mosquitto_pub -h 192.168.0.174 -t {} -m {}'.format(topic, value), shell=True)

