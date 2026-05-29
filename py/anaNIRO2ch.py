# anaNIRO2ch.py
# usage: python anaNIRO2ch.py <.nx2 FileName>
# e.g. : python anaNIRO2ch.py NIRO2chSample

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import re

def funcdetectEvent(t,dat):
    xEvent = 0
    nd = len(dat)
    y = dat.isnull()
    for it in range(nd):
        if y[it] != 1:
            tmp=re.findall(r'EVNT',dat[it])
            if len(tmp)>0:
                xEvent=np.append(xEvent, t[it])
    return xEvent[1:]

def funcMinMax(*dat):
    tmpMin = 0
    tmpMax = 0
    for v in dat:
        min = np.min(v)
        max = np.max(v)
        if min<tmpMin:
            tmpMin = min
        if max>tmpMax:
            tmpMax = max
    res = [tmpMin, tmpMax]
    return res

def funcSavefig(t, OHb, HHb, TOI, tEvent, chNo, fname='resNIRS'):
    valMinMax = funcMinMax(OHb,HHb)
    dHb = 
    cHb = 
    plt.figure(chNo)
    plt.subplot(3,1,1)
    plt.
    plt.
    plt.title('ch.{}'.format(chNo))
    plt.legend() 
    plt.ylabel('Hb [umol/L]')
    plt.subplot(3,1,2)
    plt.
    plt.plot(t,cHb,color='g',label='OHb+HHb')
    plt.ylabel('dHb, cHb [umol/L]')
    plt.legend()
    plt.subplot(3,1,3)
    plt.plot(t,TOI)
    plt.ylabel('TOI [%]')
    for i in range(3):
        plt.subplot(3,1,1+i)
        plt.grid()
        for timing in tEvent:
            if i<2:
                plt.plot([timing,timing],valMinMax,'k--')
            else:
                plt.plot([timing,timing],[60,100],'k--')
    plt.xlabel('Time [s]')  
    plt.pause(5)
    plt.savefig('{}_results_ch{}.png'.format(fname,chNo))

if __name__=='__main__':
    args = sys.argv
    fname=args[1]
    print('... Loading {}'.format(args[1]))
    dat = pd.read_csv('{}.nx2'.format(fname), header=13, encoding='cp932')
    t=dat['elpsec']
    OHb1=
    HHb1=
    TOI1=dat['TOI_1']
    OHb2=dat['O2Hb_2']
    HHb2=dat['HHb_2']
    TOI2=dat['TOI_2']
    ERR=dat['Comment']

    tEvent = funcdetectEvent(t,ERR)

    funcSavefig(t, OHb1, HHb1, TOI1, tEvent, 1, fname)
    funcSavefig(t, OHb2, HHb2, TOI2, tEvent, 2, fname)
# end of file