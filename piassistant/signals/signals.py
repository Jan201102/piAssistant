import logging
from piassistant.Isignals import Isignals
from multiprocessing import Process
import time
import platform


class Signals(Isignals):
    def __init__(self,**config):
        self.platform = platform.system()
        if self.platform == "Linux":
            board = __import__("board")
            neopixel = __import__("neopixel")
            pixelPin = board.D10
            self.numPixels = 24
            self.ORDER = neopixel.GRB
            self.pixels = neopixel.NeoPixel(pixelPin, self.numPixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER)
            self.p = Process(target=self.wait)
            self.p.start()
        
    def wait(self):
        while True:
            time.sleep(1)
    
    def PixelDriver(self, state: str, progress = 0):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        if state == "activate":
            for i in range(int(self.numPixels/2)):
                self.pixels[i] = (0, 255, 125)
                self.pixels[self.numPixels-1-i] = (0, 255, 125)
                self.pixels.show()
                time.sleep(0.02)
                
        elif state == "deactivate":
            pass
        
        elif state == "processing":
            while True:
                self.rainbow_cycle(0.003)
        
        elif state == "startup":
            for i in range(int(self.numPixels*progress/100)):
                self.pixels[i] = (255,0,0)
                self.pixels.show()
                
        elif state == "startupSuccess":
            self.pixels.fill((0, 255, 0))
            self.pixels.show()
            time.sleep(1)
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
        
        self.wait()
        
    def set_state(self, state: str, progress: int = 0):
        if self.platform == "Linux":
            logging.debug(f"setting signals to {state}")
            self.p.terminate()
            self.p.join()
            self.p = Process(target=self.PixelDriver, args=(state, progress,))
            self.p.start()
        
    def activate(self):
        self.set_state("activate")

    def deactivate(self):
        self.set_state("deactivate")
        
    def showProcessing(self):
        self.set_state("processing")
        
    def showStartup(self,progress):
        self.set_state("startup",progress)
    
    def showStartupSuccess(self):
        self.set_state("startupSuccess")
        

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.numPixels):
                pixel_index = (i * 256 // self.numPixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)
        

if __name__ == "__main__":
    print("start")
    s = Signals("on")
    s.showStartup(50)
    time.sleep(5)
    print("StartSucess")
    s.showStartupSuccess()
    time.sleep(5)
    print("activate")
    s.activate()
    time.sleep(5)
    print("processing")
    s.showProcessing()
    time.sleep(5)
    print("off")
    s.deactivate()
    time.sleep(1)
    s.p.terminate()