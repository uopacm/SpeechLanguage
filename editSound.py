from pydub import AudioSegment

# Testing purpose
audio = AudioSegment.from_wav("test.wav")

# Time is in milliseconds
def trimAudio(audio, timeLeft, timeRight):
    newSound = audio[timeLeft:len(audio) - timeRight]
    newSound.export("testResult.wav", format="wav")

# Add more functionality if needed

#trimAudio(audio, 1000, 0) # Testing

