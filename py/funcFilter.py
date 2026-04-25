import numpy as np
from scipy.signal import butter, lfilter, filtfilt, bode, TransferFunction
import matplotlib.pyplot as plt

def func_bode(num, den, Fc=None, wvec=np.logspace(-3, 3)):
    s = TransferFunction(num, den)
    w, mag, phase = bode(s, wvec)
    f = w/(2*np.pi)
    plt.figure(figsize=(12,5))
    #plt.subplot(1,2,1)
    plt.semilogx(f, mag)
    if Fc is not None:
        plt.semilogx([Fc, Fc],[np.min(mag), 3],'k--')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude [dB]')
    plt.grid()
    plt.show()

def func_analogLPF(order, Fc):
    b,a = butter(order, 2*np.pi*Fc, btype='low', analog=True)
    fvec = np.logspace(-2, 3, 50)
    wvec = fvec * np.pi
    func_bode(b,a,Fc,wvec)

def func_analogHPF(order, Fc):
    b,a = butter(order, 2*np.pi*Fc, btype='high', analog=True)
    fvec = np.logspace(-2, 3, 50)
    wvec = fvec * np.pi
    func_bode(b,a,Fc,wvec)

class bwfilter:
	def funcLPF(self, x, Fc, Fs, order=4, swanalog=False):
		Fnq = Fs/2
		nFc = Fc/Fnq
		b,a = butter(order, nFc, btype='low', analog=swanalog)
		#y = lfilter(b,a,x)
		y = filtfilt(b,a,x)
		return y

	def funcHPF(self, x, Fc, Fs, order=4, swanalog=False):
		Fnq = Fs/2
		nFc = Fc/Fnq
		b,a = butter(order, nFc, btype='high', analog=swanalog)
		#y = lfilter(b,a,x)
		y = filtfilt(b,a,x)
		return y

	def funcBPF(self, x, Fc1, Fc2, Fs, order=4, swanalog=False):
		Fnq = Fs/2
		nFc1 = Fc1/Fnq
		nFc2 = Fc2/Fnq
		b,a = butter(order, [nFc1, nFc2], btype='bandpass', analog=swanalog)
		print('den={},  num={}'.format(a,b))
		#y = lfilter(b,a,x)
		y = filtfilt(b,a,x)
		return y

	def funcBEF(self, x, Fc1, Fc2, Fs, order=5, swanalog=False):
		Fnq = Fs/2
		nFc1 = Fc1/Fnq
		nFc2 = Fc2/Fnq
		b,a = butter(order, [nFc1, nFc2], btype='bandstop', analog=swanalog)
		#y = lfilter(b,a,x)
		y = filtfilt(b,a,x)
		return y
		
if __name__=='__main__':
	print('This is a module file')
