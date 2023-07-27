import pyaudio
import wave


class AudioPlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.chunk = 1024

    def __del__(self):
        self.p.terminate()

    def play_wave(self, file):
        'open wave file'
        wf = wave.open(file, 'rb')

        'open stream'
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)

        data = wf.readframes(self.chunk)

        'play audio'
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(self.chunk)

        'stop stream'
        stream.stop_stream()
        stream.close()


if __name__ == '__main__':
    a = AudioPlayer()
    a.play_wave('../302215296.wav')
