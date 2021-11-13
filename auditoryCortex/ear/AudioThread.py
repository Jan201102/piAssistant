from queue import Queue
from threading import Thread
import logging


class AudioThread:
    def __init__(self, stream, chunk, timeout=0, rate=16000):
        self.run = True
        self.queue = Queue(maxsize=0)
        self.thread = Thread(target=self.read_stream, args=(stream, chunk, rate, timeout))
        self.thread.start()
        while self.queue.empty():
            pass

    def stop(self, verbose=0):
        self.run = False
        try:
            logging.info('waiting for Thread to finish...')
            self.thread.join()
            logging.info('Done')
        except:
            pass

    def read_stream(self, stream, CHUNK, rate, timeout=0):
        if timeout == 0:
            while self.run:
                data = stream.read(CHUNK, exception_on_overflow=False)
                self.queue.put(data)
        else:
            for _ in range(round(timeout * rate / CHUNK)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                self.queue.put(data)
            self.run = False

    def get(self):
        if not self.queue.empty() or self.run != False:
            return self.queue.get()

        return None
