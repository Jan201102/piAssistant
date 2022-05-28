"""
clock Plugin
enables a timer with a range of 2 to 99 minutes.
"""

import threading
import pygame
import time

class Plugin:
    def __init__(self,*args,**kwargs):
        self.einer = ['null', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun']
        self.zehner = ['null','zehn', 'zwanzig', 'dreißig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig']
        self.faktor = ['hundert', 'tausend']
        self.vorsilbe = ['null', 'ein', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun']
        pass

    def process(self,command):
        splitCommand = command.split(" ")
        keywords = ["timer","wecker"]
        one = 0
        ten = 0
        number = None
        testKeyword = False
        for keyword in keywords:
            if keyword in command:
                testKeyword = True

        if testKeyword is True:
            for word in splitCommand:
                for i,a in enumerate(self.zehner):
                    if a in word:
                        ten = i
                        for c,b in enumerate(self.vorsilbe):
                            if b in word:
                                one = c

                if ten == 0:
                    for i,a in enumerate(self.einer):
                        if a in word:
                            one = i
                if "elf" in word:
                    ten = 1
                    one = 1
                if "zwölf" in word:
                    ten = 1
                    one = 2

            number = ten * 10 + one
            thread = threading.Thread(target=self.alarm, args=(number,))
            thread.start()
            return("Ich stelle einen timer auf {} minuten".format(number))


    def alarm(self,duration):
        for _ in range(duration*60):
            time.sleep(1)
        print("alarm")
        pygame.mixer.init()
        pygame.mixer.music.load('./plugins/alarm_classic.mp3')
        pygame.mixer.music.play()

if __name__ == "__main__":
    c = Plugin()
    for i in ["fünf","drei","dreiundzwanzig","fünfundsechzig"]:
        num = c.process("dummy",i+" timer")
        print(num)
