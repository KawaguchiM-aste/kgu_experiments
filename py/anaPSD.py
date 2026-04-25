import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
from scipy.signal import welch
#from spectrum import *

class PSD:
  def funcPwelch(self,t,x):
    Fs = 1/np.mean(np.diff(t))
    f,p = welch(x,Fs,nperseg=int(len(x)/8))
    return f,p
  
  def funcPar(self,t,x,maxorder=40):
    #Fs = 1/np.mean(np.diff(t))
    #order = arange(1,maxorder)
    #rho = [aryule(x,i)[1] for i in order]
    #aic = AIC(len(x), rho, order)
    #ind = np.argmin(aic)
    #k = order[ind]
    #print(' AR fitting, order= {}'.format(k))
    #p = pyule(x, k, sampling=Fs)
    #f = p.frequencies()
    #pp = p.psd
    #pptotal = np.trapz(pp,f)
    #ppt = np.trapz(x**2,t)/len(t)
    #pp = pp*ppt/pptotal
    #return f, pp
    return 0,0

  def funcRelPower(self,t,xraw,frange,sw=0,fname_export='PSD'):
    anaPsd = PSD()
    nrange = frange.shape[0]
    Pabs = np.zeros(nrange)
    Prel = np.zeros(nrange)
    x = xraw-np.mean(xraw)
    f,p = anaPsd.funcPwelch(t,x)
    #f,p = anaPsd.funcPar(t,x)
    Fs = 1/np.mean(np.diff(t))
    Ptotal = np.trapz(p,f)
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(t,x)
    plt.xlabel('Time [s]')
    plt.subplot(2,1,2)
    plt.plot(f, p)
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(1/(np.max(t)), Fs/2)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD')
    for i in range(nrange):
      ind1 = np.min(np.argwhere(f>=frange[i,0]))
      ind2 = np.max(np.argwhere(f<=frange[i,1]))+2
      c = list(np.random.choice(range(256), size=3)/256)
      plt.fill_between(f[ind1:ind2], p[ind1:ind2], facecolor=c, alpha=0.5)
      Pabs[i] = np.trapz(p[ind1:ind2],f[ind1:ind2])
      Prel[i] = Pabs[i]/Ptotal
    if sw==1:
      plt.pause(3)
      plt.savefig('{}_PSD.png'.format(fname_export))
    return Pabs, Prel
    
if __name__=='__main__':
  anaPsd = PSD()
  args = sys.argv
  fname=args[1]
  print('... Loading {}'.format(args[1]))
  dat = pd.read_csv('{}.csv'.format(fname))
  n = int(dat.size/2)
  a = dat.values.reshape(n,2)
  t = a[:,0]
  x = a[:,1]
  xv = x-np.mean(x)
  #f,p=anaPsd.funcPar(t,xv)
  frange=np.array([[0.05, 0.15],[0.15, 0.4]])
  anaPsd.funcRelPower(t,x,frange,1)
# end of file  