# usage: python ana_avepsd.py results_hoge1_ACC results_hoge2_ACC results_hoge3_ACC
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from 
import sys
import datetime

if __name__=='__main__':
    n = 100
    fnew = np.linspace(0, 1.25, n)
    args = sys.argv
    nfiles = len(args[1:])
    Pnew = np.zeros((n,nfiles))
    Pave = np.zeros((n,2))
    for i in range(nfiles):
        c = i/nfiles
        fname = args[1+i]
        print('... [Loading] {}.xlsx'.format(fname))
        df = pd.read_excel('{}.xlsx'.format(fname), sheet_name='psd',header=None)
        f = df.iloc[:,0]
        p = df.iloc[:,1]
        f = 
        ptmp = f(fnew)
        Pnew[:,i] = ptmp
        plt.subplot(1,2,1)
        plt.plot(fnew, ptmp, color=[c, 0, 1-c],  alpha=0.6)

    for i in range(n):
        Pave[i,0] = np.mean(Pnew[i,:])
        Pave[i,1] = np.std(Pnew[i,:])
    plt.subplot(1,2,1)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD')
    plt.subplot(1,2,2)
    plt.errorbar(fnew, Pave[:,0],yerr=Pave[:,1], ecolor='c')
    plt.plot(fnew, Pave[:,0], 'k-')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.xlabel('Frequency [Hz]')
    plt.pause(3)
    now=datetime.datetime.now()
    exfname='gait_psd_'+now.strftime('%Y-%m-%d-%H-%M')
    plt.savefig('{}.png'.format(exfname))
    print('[Exported] {}.png'.format(exfname))
    fnew = fnew.reshape(n,1)
    df = pd.DataFrame(np.concatenate([fnew, Pnew, Pave],1))
    dff = pd.DataFrame(args[1:])
    with pd.ExcelWriter('{}.xlsx'.format(exfname), engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=False, sheet_name='psd')
        dff.to_excel(writer, index=False, header=False, sheet_name='files')
    print('[Exported] {}.xlsx'.format(exfname))
# end of file