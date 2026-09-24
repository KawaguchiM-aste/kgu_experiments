# usage: python ana_gait.py hoge_ACC
# Required files: anaECG, anaPSD, funcFilter
import pandas as pd
import numpy as np
#import scipy.stats
from scipy import interpolate, stats
import random
from matplotlib import pyplot as plt
import sys
import anaECG
import anaPSD
import funcFilter

def func_reject_out(timings, tmax=1.4):
    # 外れ値(tmaxより大きな値)を除去
    T = np.diff(timings)
    t_old = timings[1:]
    v = [0]
    T_new = [0]
    t_new = [0]
    for i in range(len(T)):
        if T[i]>=tmax:
            v.append(i)
    if len(v)>=2:
        T_new = T.tolist()
        t_new = t_old
        v_new = v[1:]
        for i in range(len(v_new)):
            try:
                print('...[removed] {:.3f}'.format(T[v_new[i]]))
                T_new.remove(T[v_new[i]])
                t_new.remove(t_old[v_new[i]])   
            except ValueError:
                print('...[passed ] {:.3f}'.format(T_new[v_new[i]]))
                pass
            except IndexError:
                print('...[passed ] Index out of range...')
                if len(T_new)<len(t_new):
                    t_new = t_new[0:len(T_new)]
                elif len(t_new)<len(T_new):
                    T_new = T_new[0:len(t_new)]
                pass
    else:
        T_new = T
        t_new = t_old
    return t_new, T_new

def func_RRI_stat(tR, tmaxperi=1.4, sw=0, fname_export='stat_Twalk'):
    #anaECGのコードからCopy&Pasteして, 一部改変する
    tRnew, RRI = func_reject_out(tR, tmax=tmaxperi)
    mRRI = 
    SD_RRI = 
    s='RRI: Mean={:.3f}[s], SD={:.3f}[s]'.format(mRRI, SD_RRI)
    if sw==1:
        plt.figure(figsize=[8,4])
        plt.subplot(1,3,1)
        plt.stem(tRnew, RRI)
        plt.xlabel('Time [s]')
        plt.ylabel('Walking Cycle[s]')
        plt.ylim(np.min(RRI),np.max(RRI))
        plt.subplot(1,3,2)
        plt.boxplot(RRI, labels=[' '], showmeans=True)
        plt.subplot(1,3,3)
        anaECG.func_draw_hist(RRI)
        plt.xlabel('# of Walk')
        plt.title(s)
        plt.pause(3)
        plt.savefig('{}_Wstat.png'.format(fname_export))
        print('[Exported] {}_Wstat.png'.format(fname_export))
    return mRRI, SD_RRI, tRnew, RRI

def func_find_peaks(x, Fs, tdead=0.3, vth=1.0):
    # ピーク検出
    itdead = int(tdead*Fs)
    nd = len(x)
    it = 1
    tp = [0]
    while it<nd-1:
        if it<3*itdead:
            ittmp = np.argmax(x[:3*itdead])
            tp.append(ittmp)
            it = it+ittmp+itdead
        else:
            if x[it]>x[it-1] and x[it]>x[it+1] and x[it]>vth:
                xmax = np.max(x[it-itdead:it+itdead])
                if x[it] == xmax:
                    tp.append(it)
                    it = it+itdead+1
                else:
                    iit = it
                    while iit<it+itdead and iit<nd:
                        if x[iit] == xmax:
                            tp.append(iit)
                            it = it+int(np.abs(iit-it))+1
                            iit=iit+itdead
                        else:
                            iit = iit+1
                    it = it+itdead+1
            else:
                it = it+1
    tp = list(set(tp))
    tp = tp[1:]
    tp = sorted(tp)
    tpeaks = [0]
    for i in range(len(tp)):
        tpeaks.append(tp[i]/Fs)
    tpeaks=tpeaks[1:]
    return tp, tpeaks

def func_walk(y, t, t_win=10, tdead=0.7, fname='result'):
    F = funcFilter.bwfilter()
    dt = np.mean(np.diff(t))
    Fs = 1/dt
    tshow=(np.max(t)-t_win)*random.random()
    itshow=[int(tshow*Fs),int((tshow+t_win)*Fs)]
    yf= 
    yf= 
    itpeaks,tmax = func_find_peaks(yf, Fs, tdead=tdead)
    plt.figure(figsize=[12,5])
    plt.subplot(2,1,1)
    plt.plot(t,y,'k-',alpha=0.2)
    plt.plot(t,yf,'b-')
    plt.plot(t[itshow[0]:itshow[1]],yf[itshow[0]:itshow[1]],'r')
    plt.ylabel('z-score(ACC)')
    plt.xlim(np.min(t),np.max(t))
    plt.subplot(2,1,2)
    plt.plot(t,y,'k-',alpha=0.2)
    plt.plot(t,yf,'b-')
    plt.plot(t[itshow[0]:itshow[1]],yf[itshow[0]:itshow[1]],'r')
    for i in itpeaks:
        if t[i]>=tshow and t[i]<tshow+t_win:
            plt.text(t[i], yf[i], 'p')
    plt.ylabel('z-score(ACC)')
    plt.xlim(tshow, tshow+t_win)
    plt.xlabel('Time [s]')
    plt.pause(1)
    exfname='{}_time.png'.format(fname)
    plt.savefig(exfname)
    print('[Exported] {}'.format(exfname))
    return yf, tmax

def func_interp(tR, RRI, Fs=2.5, algo='linear', sw=0):
    #anaECGのコードからCopy&Pasteして, 一部改変する
    # algo: 'linear', 'nearest', 'cubic', 'lagrange'
    dt = 1/Fs
    t = np.arange(np.min(tR), np.max(tR), dt)
    if algo=='lagrange':
        f = interpolate.lagrange(tR, RRI)
    else:
        f = interpolate.interp1d(tR, RRI, kind=algo)
    RRIT = f(t)
    if sw==1:
        plt.figure(figsize=[8,2])
        plt.plot(tR,RRI,'cs', alpha=0.6, label='RRI')
        plt.plot(t,RRIT,'b.-', label='Interpolation@'+algo)
        plt.xlabel('Time [s]')
        plt.ylabel('Walking Cycle[s]')
        plt.legend()
        plt.pause(3)
    return RRIT, t

def func_draw_psd(x, t, fname_export='result_PSD'):
    Psd = anaPSD.PSD()
    y = x-np.mean(x)
    freq, p = Psd.funcPwelch(t, y, nseg=4)
    plt.figure(figsize=[5,8])
    plt.subplot(3,1,1)
    plt.plot(t,y)
    plt.xlabel('Time [s]')
    plt.ylabel('Cycle trend [s]')
    plt.subplot(3,1,(2,3))
    plt.plot(freq, p)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD')
    plt.grid()
    plt.pause(2)
    exfname='{}_psd.png'.format(fname_export)
    plt.savefig(exfname)
    print('[Exported] {}'.format(exfname))
    return p, freq

def func_normalize_cycle(x, t, timings, tmax=1.4, fname_export='result_norm'):
    dtn = 0.2
    progre = 0
    tnorm = np.arange(0, 100, dtn)
    ndn = len(tnorm)
    nd = len(t)
    n = len(timings)-1
    X = np.zeros((ndn, n))
    xave = np.zeros((ndn,2))
    trange = np.zeros(2)
    v = np.zeros(2, dtype = int)
    plt.figure(figsize=[7,10])
    for i in range(n):
        c = i/n
        trange[0] = timings[i]
        trange[1] = np.min([timings[i+1], trange[0]+tmax])
        for j in range(2):
            for it in range(nd-1):
                if t[it]<=trange[j] and t[it+1]>trange[j]:
                    v[j] = it
        tq = np.linspace(t[v[0]], t[v[1]], ndn)
        xq = np.interp(tq, t[v[0]:v[1]], x[v[0]:v[1]])
        X[:,i] = xq
        plt.subplot(4,1,1)
        plt.plot(t[v[0]:v[1]]-t[v[0]], x[v[0]:v[1]], color=[c, 0, 1-c], alpha=0.3)
        plt.subplot(4,1,2)
        plt.plot(tnorm, xq, color=[c, 0, 1-c], alpha=0.3)
        if c*100>=progre:
            plt.subplot(4,1,1)
            plt.title('{:.1f}[%] (n={})'.format(c*100, n))
            plt.pause(.01)
            progre = progre+11
    for it in range(ndn):
        xave[it,0] = np.mean(X[it,:])
        xave[it,1] = np.std(X[it,:])
    plt.subplot(4,1,1)
    plt.xlabel('Time [s]')
    plt.title('n={}'.format(n))
    plt.subplot(4,1,(3,4))
    plt.errorbar(tnorm, xave[:,0],yerr=xave[:,1],ecolor='c')
    plt.plot(tnorm, xave[:,0], 'k-')
    plt.xlabel('Normalized Time [%]')
    plt.pause(1)
    exfname='{}_tnorm.png'.format(fname_export)
    plt.savefig(exfname)
    print('[Exported] {}'.format(exfname))
    return tnorm, X, xave

if __name__=='__main__':
    args = sys.argv
    fname=args[1]
    amp_acc = 1
    if len(args)>2:
        amp_acc = float(args[2])
    print('... [Loading] {}.xlsx'.format(fname))
    df = pd.read_excel('{}.xlsx'.format(fname))
    n = int(df.size/2)
    a = df.values.reshape(n,2)
    t = a[:,0]
    dt = np.mean(np.diff(t))
    Fs = 1/dt
    x_ACC = amp_acc*a[:,1]

    # 処理の開始
    z = stats.zscore(x_ACC)
    zf, tim = func_walk(z, t, tdead=0.75, fname=fname)
    m, s, timings, T = func_RRI_stat(tim, tmaxperi=1.4, sw=1, fname_export=fname)
    Ttrend, t_trend = func_interp(timings, T)
    p, freq = func_draw_psd(Ttrend, t_trend, fname_export=fname)
    tnorm, Z, zave = func_normalize_cycle(z, t, timings, fname_export=fname)
    
    # Excelファイル出力
    ndr = len(t)
    t = t.reshape(ndr,1)
    z = z.reshape(ndr,1)
    dfr = pd.DataFrame(np.concatenate([t,z],1))
    ne = len(T)
    timings = np.array(timings).reshape(ne,1)
    T = np.array(T).reshape(ne,1)
    dfe = pd.DataFrame(np.concatenate([timings, T],1))
    nd = len(Ttrend)
    Ttrend = Ttrend.reshape(nd,1)
    t_trend = t_trend.reshape(nd,1)
    dft = pd.DataFrame(np.concatenate([t_trend, Ttrend],1))
    ndn = len(tnorm)
    tnorm = tnorm.reshape(ndn,1)
    dfn = pd.DataFrame(np.concatenate([tnorm, Z],1))
    dfna = pd.DataFrame(np.concatenate([tnorm, zave],1))
    nf = len(freq)
    p = p.reshape(nf,1)
    freq = freq.reshape(nf,1)
    dfp = pd.DataFrame(np.concatenate([freq,p],1))
    exfname = 'results_{}.xlsx'.format(fname)
    with pd.ExcelWriter(exfname, engine='openpyxl') as writer:
        #dfr.to_excel(writer, index=False, header=None, sheet_name='z')
        dfe.to_excel(writer, index=False, header=None, sheet_name='timings')
        dft.to_excel(writer, index=False, header=None, sheet_name='trend')
        dfn.to_excel(writer, index=False, header=None, sheet_name='z_timings')
        dfna.to_excel(writer, index=False, header=None, sheet_name='z_timings_average')
        dfp.to_excel(writer, index=False, header=None, sheet_name='psd')
    print('[Exported] {}'.format(exfname))
    # end of file