"""
timer app
enables a timer with a range of 2 to 99 minutes.
"""

import threading
import pygame
import time
import os


class App:
    def __init__(self):
        self.templateFolder = os.path.join(os.path.dirname(__file__), "./templates")

    def set(self, duration):
        duration = duration.replace(" ","")
        duration = time.strptime(duration, "%H:%M:%S")
        duration = duration.tm_hour*3600 + duration.tm_min*60 + duration.tm_sec
        timer = threading.Thread(target=self.alarm, args=(duration,))
        timer.start()

    def alarm(self, duration: int):
        time.sleep(duration)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(self.templateFolder, "alarm_classic.mp3"))
        pygame.mixer.music.play()
