from __future__ import division
from numpy.fft import rfft
from numpy import argmax, sqrt, mean, diff, log
from scipy.signal import blackmanharris
from time import time
import sys

from parabolic import parabolic


def freq_from_fft(sig, fs):
    """Estimate frequency from peak of FFT
    
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * blackmanharris(len(sig))
    f = rfft(windowed)
    
    # Find the peak and interpolate to get a more accurate peak
    i = argmax(abs(f)) # Just use this for less-accurate, naive version
    true_i = parabolic(log(abs(f)), i)[0]
    
    # Convert to equivalent frequency
    return fs * true_i / len(windowed)

filename = sys.argv[1]

print 'Reading file "%s"\n' % filename
signal, fs, enc = flacread(filename)

print 'Calculating frequency from FFT:',
start_time = time()
print '%f Hz'   % freq_from_fft(signal, fs)
print 'Time elapsed: %.3f s\n' % (time() - start_time)