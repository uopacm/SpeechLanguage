import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

spf = wave.open('test.wav', 'r')

signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

if spf.getnchannels() == 2:
	print('Just mono files')
	sys.exit(0)

plt.figure(1)
plt.title('Signal wave..')
plt.plot(signal)
plt.savefig('test.png')