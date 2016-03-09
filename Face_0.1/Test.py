#!/usr/bin/env python
"""
Mosquito Ringtone Detector

Detects the Mosquito ringtone via a microphone.

Author: Jason Locklin
	http://artsweb.uwaterloo.ca/~jalockli

You are free to Copy, Modify and Redistribute the following program
under the General Public License Version 3: 
           http://www.gnu.org/licenses/gpl.html
"""

# Required Python libraries
import pyaudio
from numpy import zeros,linspace,short,fromstring,hstack,transpose
from scipy import fft
from time import sleep
import sys
import wave

#Set up audio sampler
NUM_SAMPLES = 2048
SAMPLING_RATE = 44100
SPECTROGRAM_LENGTH = 100


wa  wave.open(sys.argv[1], 'rb')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

while True:
   while stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
   audio_data  = fromstring(stream.read(stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
   normalized_data = audio_data / 32768.0
   intensity = abs(fft(normalized_data))[:NUM_SAMPLES/2]
   frequencies = linspace(0.0, float(SAMPLING_RATE)/2, num=NUM_SAMPLES/2)
   print frequencies
   sleep(0.01)





