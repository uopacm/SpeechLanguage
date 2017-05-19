import pyaudio
import wave
import threading
import struct
import numpy

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

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

    def play(self, file_path, start):
        if not self.is_playing:
            self.is_playing = True
            # open wave file
            track = wave.open(file_path, 'rb')
            start *=  track.getnframes() /  float(track.getframerate())
            
            # initialize audio
            py_audio = pyaudio.PyAudio()
            self.stream = py_audio.open(format=py_audio.get_format_from_width(track.getsampwidth()),
                       channels=track.getnchannels(),
                       rate=track.getframerate(),
                       output=True)

            # skip unwanted frames
            
            n_frames = int(start * track.getframerate())
            chunk_size = track.getnchannels() * track.getsampwidth()

            clip = track.readframes(track.getnframes())[n_frames * chunk_size:]

            # write desired frames to audio buffer
            data = list(chunks(clip, self.CHUNK))
            def audio_thread():
                for frame in data:
                    if not self.is_playing:
                        break
                    self.stream.write(frame)
                    
            self.play_thread = threading.Thread(target=audio_thread)
            self.play_thread.start()

    def stop(self):
        if(self.is_playing):
            self.is_playing = False
            self.stream.stop_stream()
            self.stream.close()
            self.play_thread.join()
            self.audio_buffer = []

    
            
