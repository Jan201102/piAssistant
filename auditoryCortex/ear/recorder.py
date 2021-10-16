import wave


class Recorder:
    def __init__(self, samprate, channels, samp_size):
        self.samprate = samprate
        self.channels = channels
        self.samp_size = samp_size
        self.frames = []

    def new_record(self):
        self.frames = []
    def record(self, frame):
        self.frames.append(frame)

    def save_recording(self, name=None):
        if len(self.frames) != 0:
            if name is None:
                name = str(hash(tuple(self.frames))) + '.wav'

            wave.open(name,'wb')
            wf = wave.open(name, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.samp_size)
            wf.setframerate(self.sampRate)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            return name
        return