import logging
from .Isignals import Isignals
import board
import neopixel
from multiprocessing import Process
import time


class Signals(Isignals):
    def __init__(self, **config):
        pixelPin = board.D18
        self.numPixels = 24
        ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(pixelPin, self.numPixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
        self.process = Process(target=self.wait)
        self.process.start()
        
    def wait(self):
        while True:
            pass
    
    def PixelDriver(self, state: str):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        if state == "activate":
            for i in range(self.numPixels):
                self.pixels[i] = (255, 0, 0)
                self.pixels.show()
                time.sleep(0.05)
                
        elif state == "deactivate":
            pass
        
        elif state == "startup":
            while True:
                self.pixels.fill((255, 0, 0))
                self.pixels.show()
                time.sleep(0.5)
                self.pixels.fill((0, 0, 0))
                self.pixels.show()
                time.sleep(0.5)
                
        elif state == "startupSuccess":
            self.pixels.fill((0, 255, 0))
            self.pixels.show()
            time.sleep(1)
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
        
        self.wait()
        
    

    def activate(self):
        self.process.terminate()
        self.process.join()
        self.p = Process(target=self.PixelDriver, args=("activate",))
        self.p.start()
        logging.debug("light up LED")

    def deactivate(self):
        self.process.terminate()
        self.process.join()
        self.p = Process(target=self.PixelDriver, args=("deactivate",))
        self.p.start()
        logging.debug("turn off LED")
        
    def showProcessing(self):
        self.process.terminate()
        self.process.join()
        self.p = Process(target=self.PixelDriver, args=("processing",))
        self.p.start()
        
    def showStartup(self):
        self.process.terminate()
        self.process.join()
        self.p = Process(target=self.PixelDriver, args=("startup",))
        self.p.start()
    
    def showStartupSuccess(self):
        self.process.terminate()
        self.process.join()
        self.p = Process(target=self.PixelDriver, args=("startupSucess",))
        self.p.start()
    

if __name__ == "__main__":
    s = Signals()
    s.showStartup()
    time.sleep(5)
    s.showStartupSuccess()
    time.sleep(5)
    s.activate()
    time.sleep(5)
    s.showProcessing()
    time.sleep(5)
    s.deactivate()