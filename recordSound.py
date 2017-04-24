import pyaudio
import wave
import threading

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class AudioRecorder:
    def __init__(self):

        self.output = "sound.wav"
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, start=False)
        self.audio_buffer = []
        self.recording_thread = {}
        
#    def __del__(self):
#        self.stream.close()
#        self.audio.terminate()
                
    def recordAudio(self):
        while(self.is_recording):
            data = self.stream.read(CHUNK)
            self.audio_buffer.append(data)

    def start_recording(self, filepath):
        self.is_recording = True
        self.output = filepath
        self.recording_thread = threading.Thread(target=self.recordAudio)
        self.stream.start_stream()
        self.recording_thread.start()

                                                 
    # If recording, stops stream and writes buffer to file
    def stop_recording(self):
        if(self.is_recording):
            self.is_recording = False
            self.recording_thread.join()
            self.stream.stop_stream()

            # Write to file
            wf = wave.open(self.output, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.audio_buffer))
            wf.close()

            # Clear buffer
            self.audio_buffer = []
            

        
    

