# anaEMG.py
# usage: python anaEMG.py <Excel_file>
# e.g. : python exportOpenSignals.py opensignals20XX_EMG

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
from biosppy.signals import emg
from scipy import signal

Fc = 5.0  #　Cut-off frequency for LPF

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

def func_mvc(x, xenv, t, Fs):
    flag = 0
    print('*** calc. MVC ***')
    while flag == 0:
        plt.cla()
        plt.plot(t, x, 'k-', linewidth=0.5, alpha=0.2)
        plt.plot(t, xenv, 'b-', linewidth=1)
        plt.pause(2)
        t_start = input('t_onset: ')
        it_start = int(float(t_start)*Fs)
        t_end = input('t_end: ')
        it_end = int(float(t_end)*Fs)
        plt.plot(t[it_start:it_end], xenv[it_start:it_end], 'r-', linewidth=2)
        plt.xlabel('Time [s]')
        plt.pause(2)
        tmp = input('Press [Y], then mvc will be calculated. : ')
        if tmp.lower() == 'y':
            flag = 1
    rmsEMG = np.sqrt(np.mean(xenv[it_start:it_end]**2))
    plt.plot([t[it_start],t[it_end]], [rmsEMG, rmsEMG], 'c--', label='RMS: {:.3f}'.format(rmsEMG))  
    plt.legend()
    plt.pause(3)
    return rmsEMG

if __name__=='__main__':
    args = sys.argv
    fname = args[1]
    print('... Loading {}'.format(fname))
    dat = pd.read_excel('{}.xlsx'.format(fname),header=None, engine='openpyxl')
    t = np.array(dat.iloc[:,0])
    x = dat.iloc[:,1]

    nd = len(t)
    Fs = 1/np.mean(np.diff(t))
    y = emg.emg(signal=x, sampling_rate=Fs, show=False)
    xEMGf = y[1]

    # Envelope
    x_env, x_env_fil = func_env(xEMGf, Fc, Fs)

    # MVC
    plt.figure(2)
    rms_mvc = func_mvc(xEMGf, x_env_fil, t, Fs)
    plt.savefig('{}_mvc.png'.format(fname))
    
    # Prep. Export
    t = t.reshape(nd,1)
    xEMGf = xEMGf.reshape(nd,1)
    x_env_fil = x_env_fil.reshape(nd,1)
    x_env = x_env.reshape(nd,1)

    # Export EMG
    dfEMG = pd.DataFrame(np.concatenate([t, xEMGf, x_env_fil, x_env],1))
    exfname = '{}_fil_tim.xlsx'.format(fname)
    with pd.ExcelWriter(exfname) as writer:
        dfEMG.to_excel(writer, sheet_name='EMG', header=['Time','EMG','env(EMG)','hilbert(EMG)'], index=False)
# end of file