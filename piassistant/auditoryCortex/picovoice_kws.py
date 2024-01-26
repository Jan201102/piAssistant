import pvporcupine
from pvrecorder import PvRecorder

class PicovoiceKWS():
    def __init__(self, name="computer", picovoice_access_key = None,**kwargs):
        """
        Initializes an instance of the PicovoiceKWS class.

        Parameters:
        - keywords (list): A list of keywords to be detected.
        - access_key (str): The access key for the Picovoice platform.

        Returns:
        - None
        """
        
        self.keywords = [name]
        keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in self.keywords]
        sensitivities = [0.5] * len(keyword_paths)
        
        if picovoice_access_key == None:
            raise ValueError("AccessKey not found, please provide a valid access key for picovoice in config.json")
        
        try:
            self.porcupine = pvporcupine.create(
            access_key=picovoice_access_key,
            keyword_paths=keyword_paths,
            sensitivities=sensitivities)
        except pvporcupine.PorcupineActivationError as e:
            print("AccessKey activation error")
            raise e
        except pvporcupine.PorcupineError as e:
            print("Failed to initialize Porcupine")
            raise e

        self.recorder = PvRecorder(frame_length=self.porcupine.frame_length)
         
    def wait(self):
        """
        Waits for a keyword to be detected by the Porcupine engine.

        Returns:
            bool: True if a keyword is detected, False otherwise.
        """
        
        result = -1
        self.recorder.start()
        while result < 0:
            pcm = self.recorder.read()
            result = self.porcupine.process(pcm)
        self.recorder.stop()
        return True
    
if __name__ == "__main__":
    p = PicovoiceKWS(picovoice_access_key="your key here")
    print("waiting for keyword...")
    p.wait()