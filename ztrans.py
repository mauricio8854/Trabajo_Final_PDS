import scipy.signal as signal
from pylab import *
import matplotlib.pyplot as plt
import numpy as np

def mfreqz(b,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20 * log10 (abs(h))
    h_pot = abs(h)
    
    plt.figure(figsize=(18,8))

    subplot(211)
    plot(w/max(w),h_pot)
    ylabel('Magnitude (W)')
    xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Frequency response')

    subplot(212)
    h_Phase =  np.angle(h)  #unwrap(arctan2(imag(h),real(h)))

    plot(w/max(w),h_Phase)
    ylabel('Phase (radians)')
    #xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    title(r'Phase response')
    subplots_adjust(hspace=0.5)
    show()
    
    
def impz(num,den=1):
    l = len(num)+30
    impulse = repeat(0.,l); impulse[0] =1.
    x = arange(0,l)
    response = signal.lfilter(num,den,impulse)
    plt.figure(figsize=(18,8))
    subplot(211)
    stem(x, response)
    ylabel('Amplitude')
    xlabel(r'n (samples)')
    title(r'Impulse response')
    subplot(212)
    step = cumsum(response)
    stem(x, step)
    ylabel('Amplitude')
    xlabel(r'n (samples)')
    title(r'Step response')
    subplots_adjust(hspace=0.5)
    show()

def zeropoles(num, den=1):
    w,h = signal.freqz(num,den)
    sys1=signal.lti(num, den)
    ang=np.arange(0.0,2*np.pi,0.01)
    xp=np.cos(ang)
    yp=np.sin(ang)
    plt.figure(figsize=(10,8))
    plot(xp,yp,'--')
    plot(sys1.zeros.real, sys1.zeros.imag, 'o')
    plot(sys1.poles.real, sys1.poles.imag, 'x')
    show()

    
    
def computeZ(num, den, zeros, poles, data):
    sys1=signal.lti(num, den)
    w,h = signal.freqz(num, den)
    # agrego los polos y ceros al sistema
    zerosnew=np.hstack((sys1.zeros, zeros))
    polesnew=np.hstack((sys1.poles, poles))
    #gain=sys1.gain
    num2=np.poly(zerosnew)
    den2=np.poly(polesnew)
    #Impulse and step response
    figure(2)
    impz(num2, den2)
    show()
    #zero-poles diagrams
    zeropoles(num2, den2)
    show()
    #Frequency and phase response
    mfreqz(num2, den2)
    show()
    data2=signal.lfilter(num2, den2, data)
    subplot(211)
    plot(data)
    subplot(212)
    plot(data2)
    show()
    
