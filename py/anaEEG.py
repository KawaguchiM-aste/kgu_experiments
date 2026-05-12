# anaEEG.py
# usage: python anaEEG.py <ExcelFileName1> <Name_ch1> <ExcelFileName2> <Name_ch2>...
# e.g. : python anaEEG.py EEGsample_1-REF C3 EEGsample_2-REF C4
# required file: anaPSD.py, funcFilter.py

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import random
import datetime
import anaPSD
import funcFilter
from biosppy.signals import eeg

class anaEEG:
  def chooseEEG(self,x,Fs,chNames):
    t = x[:,0]
    nd = len(t)
    Nch = len(chNames)
    for i in range(Nch):
      y = x[:,i+1]
      plt.subplot(Nch,1,i+1)
      plt.plot(t,y)
      plt.ylabel(chNames[i])
    plt.xlabel('Time [s]')
    plt.pause(5)
    t_start = input('t_start: ')
    it_start =  int(Fs*int(t_start))
    plt.pause(5)
    t_end = input('t_end: ')
    it_end =  int(Fs*int(t_end))
    y = x[it_start:it_end,:]
    y[:,0]=y[:,0]-y[0,0]
    return x[it_start:it_end,:]
  
  def funcExtractEEG(self,x,Fs,chNames,fname_export='EEG'):
    t=x[:,0]
    tshow=(np.max(t)-3)*random.random()
    itshow=[int(tshow*Fs),int((tshow+3)*Fs)]
    plt.close('all')
    for i in range(len(chNames)):
      y = x[:,i+1]
      plt.figure(i+1)
      plt.subplot(2,1,1)
      plt.plot(t,y,'b')
      plt.plot(t[itshow[0]:itshow[1]],y[itshow[0]:itshow[1]],'r')
      plt.title(chNames[i])
      plt.subplot(2,1,2)
      plt.plot(t,y,'r')
      plt.xlim(tshow, tshow+3)
      tmp = y[itshow[0]:itshow[1]]
      plt.ylim(np.min(tmp),np.max(tmp))
      plt.xlabel('Time [s]')
      plt.pause(5)
      #plt.savefig('{}_{}.png'.format(fname_export,chNames[i]))
  
  def funcEEGPower(self,t,x,chNames,fname_ex='EEG_Power'):
    PSD = anaPSD.PSD()
    fRange = np.array([[7, 10],[9, 13],[12, 25]])
    plt.close('all')
    for i in range (len(chNames)):
      y = x[:,i+1] - np.mean(x[:,i+1])
      Pabs,Prel=PSD.funcRelPower(t,y,fRange,sw=0,fname_export=fname_ex)
      str=\
        '{}:alphaL={:.3E}, alphaH={:.3E}, beta={:.3E}, n_alphaL={:.3f}, n_alphaH={:.3f}, n_beta={:.3f}'.\
        format(chNames[i],Pabs[0],Pabs[1],Pabs[2],Prel[0],Prel[1],Prel[2])
      plt.title(str)
      plt.pause(3)
      print(str)
      plt.savefig('{}_{}.png'.format(fname_ex, chNames[i]))   

  def funcEEGPower_time(self,Fs,x,chNames,fname_ex='EEG_Power_t'):
    out = eeg.eeg(signal=x[:,1:], sampling_rate=Fs, labels=chNames, show=False)
    tt = out[2].reshape(len(out[2]),1)
    fband = ['alpha_low','alpha_High','beta']
    Nch = len(chNames)
    plt.close('all')
    for i in range(len(fband)):
      tmpdata = out[i+4]
      exfname='{}_{}'.format(fname_ex, fband[i])
      plt.figure(i)
      for j in range(Nch):
        plt.subplot(Nch,1,j+1)
        plt.plot(tt, tmpdata[:,j])
        plt.ylabel(chNames[j])
      plt.subplot(Nch,1,1)
      plt.title(fband[i])
      plt.subplot(Nch,1,Nch)
      plt.xlabel('Time [s]')
      plt.pause(3)
      plt.savefig('{}.png'.format(exfname))
      df = pd.DataFrame(np.concatenate([tt, tmpdata], 1))
      df.to_excel('{}.xlsx'.format(exfname),index=False,header=None)

if __name__=='__main__':
  EEG=anaEEG()
  F = funcFilter.bwfilter()
  args = sys.argv
  Nargs = len(args)
  chNames=[]
  now=datetime.datetime.now()
  str=now.strftime('%Y%m%d%H%M%S')
  exfname=str+'_EEG'
  j=0
  for i in range(1,Nargs):
    if i%2 ==1:
      print('... Loading {}'.format(args[i]))
      dat = pd.read_excel('{}.xlsx'.format(args[i]))
      nd = dat.shape[0]
      dat = dat.values.reshape(nd,2)
      t = dat[:,0]
      dat = np.array(dat)
      dt = np.mean(np.diff(t))
      Fs = 1/dt
      if j==0:
        x = dat
        x[:,1] = F.funcBEF(dat[:,1],48,52,Fs)
        j+=1
      else:
        dat[:,1] = F.funcBEF(dat[:,1],48,52,Fs)
        x=np.concatenate([x, dat[:,1].reshape(nd,1)],1)
    else:
      chNames.append(args[i])
  
  Nch=len(chNames)
  out = eeg.eeg(signal=x[:,1:], sampling_rate=Fs, labels=chNames, show=False)
  x[:,1:]=out[1]
  x = EEG.chooseEEG(x, Fs, chNames)
  EEG.funcExtractEEG(x,Fs,chNames,exfname)
  t = x[:,0]
  EEG.funcEEGPower(t,x,chNames,exfname)
  EEG.funcEEGPower_time(Fs,x,chNames,exfname)
# end of file