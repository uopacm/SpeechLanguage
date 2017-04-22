import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import tempfile

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
	
	#plt.savefig('test.png')
	
	temp = tempfile.NamedTemporaryFile()
	try:
		plt.savefig(temp.name)
	
	return temp

'''if __name__ == '__main__':
	generatePng('test.wav')'''