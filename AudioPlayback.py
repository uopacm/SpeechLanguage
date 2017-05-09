import pyaudio
import wave
import threading

class AudioPlayback():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    def __init__(self):
        self.is_playing = False
        self.audio = pyaudio.PyAudio()
        self.audio_buffer = []
        self.stream = {}
        self.play_thread = {}

    def play(self, file_path):
        self.is_playing = True
        f = wave.open(file_path, 'rb')
        self.stream = self.audio.open(
            format = self.audio.get_format_from_width(f.getsampwidth()),
            channels = f.getnchannels(),
            rate = f.getframerate(),
            output = True)
        self.audio_buffer = f.readframes(self.CHUNK)
        def audio_thread():
            while self.audio_buffer and self.is_playing:
                self.stream.write(self.audio_buffer)
                self.audio_buffer = f.readframes(self.CHUNK)
        self.play_thread = threading.Thread(target=audio_thread)
        self.play_thread.start()

    def stop(self):
        if(self.is_playing):
            self.is_playing = False
            self.play_thread.join()
            self.stream.stop_stream()
            self.audio_buffer = []

    
            
