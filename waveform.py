import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

def generatePng(filename):
	spf = wave.open(filename, 'r')
	
	signal = spf.readframes(-1)
	signal = np.fromstring(signal, 'Int16')
	fs = spf.getframerate()
	
	if spf.getnchannels() == 2:
		print('Just mono files')
		# sys.exit(0) # Running this in pyhcharm

	# In seconds (Algorithm taken from online)
	# Timing is extended.... test with more files
	Time = np.linspace(0, len(signal)/fs, num=len(signal))
	
	plt.figure(1)
	plt.title('Signal wave..')
	plt.plot(Time,signal)
	
	setMarkers(1, 5) # For testing
	plt.savefig('test.png')

# Set line markers for left and right side
def setMarkers(start, end):
    y_min, y_max = plt.ylim()
    plt.plot((start, start),(y_max+1, y_min-1), 'k')
    plt.plot((end, end), (y_max + 1, y_min - 1), 'k')