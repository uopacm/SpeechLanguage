import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import contextlib

# Give filename without extension
def generatePng(filename):
    with contextlib.closing(wave.open(filename + '.wav', 'r')) as spf:

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
        plt.tick_params(axis='y', which='both', left='off',labelleft='off', bottom='off', labelbottom='off')
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.axis('off')
        plt.plot(Time,signal)
        plt.tight_layout(pad=0)
        plt.savefig(filename + '.png', pad_inches=0)
