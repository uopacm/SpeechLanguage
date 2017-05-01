import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

# Give filename without extension
def generatePng(filename):
    spf = wave.open(filename + '.wav', 'r')

    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    fs = spf.getframerate()

    if spf.getnchannels() == 2:
        print('Just mono files')
    # sys.exit(0) # Running this in pyhcharm

	# In seconds (Algorithm taken from online)
	# Timing is extended.... test with more
    Time = np.linspace(0, len(signal)/fs, num=len(signal))
    plt.gcf().clear()
    plt.figure(1)
    plt.title(filename)
    plt.tick_params(axis='y', which='both', left='off',labelleft='off')
    plt.plot(Time,signal)
    plt.savefig(filename + '.png')
