# anaEMGant.py
# usage: python anaEMGant.py <Excel_file@ch.1> <Excel_file@ch.2> 
# e.g. : python exportOpenSignals.py opensignals20XX_EMG opensignals20XX_EMG1

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
from biosppy.signals import emg
from scipy import signal
import random

Fc = 5.0     # cut-off frequency [Hz]
t_win = 5.0  # time window [s]

def funcLPF(x, Fc, Fs, order=4):
    Fnq = Fs/2
    nFc = Fc/Fnq
    b,a = signal.butter(order, nFc, btype='low', analog=False)
    y = signal.filtfilt(b,a,x)
    return y

def func_env(x, Fc, Fs, show=1):
    yh = signal.hilbert(x)
    ay = np.abs(yh)
    ayf = funcLPF(ay,Fc,Fs)
    t = np.linspace(0, len(x)/Fs, len(x))
    if show == 1:
        plt.plot(t, x, 'k-', linewidth=0.5)
        plt.plot(t, ayf, 'b-', linewidth=1)
        plt.pause(2)
    return ay, ayf

if __name__=='__main__':
    args = sys.argv
    nfiles = len(args)+1
    Nch = nfiles-2
    c = 0
    
    for i in range(1,len(args)):
        fname = args[i]
        print('... Loading {}'.format(fname))
        dat = pd.read_excel('{}.xlsx'.format(fname),header=None, engine='openpyxl')
        t = np.array(dat.iloc[:,0])
        x = dat.iloc[:,1]
        nd = len(t)
        if i==1:
            y = np.zeros((nd,Nch))
            c = np.linspace(0, 1, Nch)
        if np.max(t)>t_win:
            t_start = (np.max(t)-t_win)*random.random()
        else:
            t_start = 0

        Fs = 1/np.mean(np.diff(t))
        # Raw -> High-pass filtered (HPF)
        xx = emg.emg(signal=x, sampling_rate=Fs, show=False)
        xf = xx[1]
        # HPF -> Envelope
        env, envf = func_env(xf, Fc, Fs)
        y[:,i-1] = envf

        # Draw & Export 
        plt.figure(i)
        plt.subplot(2,1,1)
        plt.plot(t, x, color=[0.2, 0.2, 0.2])
        plt.ylabel('Raw')
        plt.title('Ch.{}'.format(i))
        plt.xlim(t_start, t_start+t_win)
        plt.ylim(-0.7, 0.7)
        plt.subplot(2,1,2)
        plt.plot(t, xf, color=[0.5, 0.5, 0.5])
        plt.plot(t, envf, color=[c[i-1],0,1-c[i-1]])
        plt.ylabel('HPF & Env.')
        plt.xlim(t_start, t_start+t_win)
        plt.ylim(-0.7, 0.7)
        plt.xlabel('Time [s]')
        plt.pause(0.5)
        plt.savefig('{}_ch{}.png'.format(fname, i))

    plt.figure(Nch+1)
    for i in range(Nch):
        plt.subplot(Nch,1,i+1)
        plt.plot(t, y[:,i], color=[c[i],0,1-c[i]])
        plt.ylabel('Ch.{}'.format(i+1))
        plt.xlim(t_start, t_start+t_win)
        plt.pause(0.5)
    plt.xlabel('Time [s]')
    plt.savefig('{}.png'.format(fname[:-1]))
# end of file      