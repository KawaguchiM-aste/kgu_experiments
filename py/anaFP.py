# anaFP.py
# usage: python anaFP.py <csvFileName> <Fs_new>
# e.g. : python anaFP.py A1ari 20

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sys

class FP:
  def funcArcLength(self, x, y):
    dx=
    dy=
    dr=
    L =
    print(' ... Length: {:.3E}'.format(L))
    plt.plot(x,y,'k-')
    return L

  def funcRectArea(self, x, y):
    x1=
    x2=
    y1=
    y2=
    dx=
    dy=
    A = 
    print(' ... Rect. Area: {:.3E}'.format(A))
    plt.plot([x1, x1],[y1, y2],'b--')
    plt.plot([x2, x2],[y1, y2],'b--')
    plt.plot([x1, x2],[y1, y1],'b--')
    plt.plot([x1, x2],[y2, y2],'b--')
    return A
    
  def funcResample(self, x, Fs, Fs_new):
    interval=int(np.round(Fs/Fs_new))
    X=
    return X

if __name__=='__main__':
  fp = 
  args=sys.argv
  fname=args[1]
  Fs_new=int(args[2])
  print('... Loading {}'.format(args[1]))
  dat = pd.read_csv('{}.csv'.format(args[1]), header=8, names=\
    ('Time', 'Fx', 'Fy', 'Fz', 'COPx', 'COPy','Mx','My','Mz'))
  nd = dat.shape[0]
  x = dat.values.reshape(nd,9)
  t = x[:,0]
  Fs = 1/np.mean(np.diff(t))
  X = fp.funcResample(x, Fs, Fs_new)
  tnew=X[:,0]
  COPx=X[:,4]
  COPy=X[:,5]
  COP = 
  COP = COP.reshape(len(tnew),1)
  
  plt.figure(1)
  plt.subplot(3,1,1)
  plt.
  plt.ylabel('COPx [mm]')
  plt.subplot(3,1,2)
  plt.
  plt.ylabel('COPy [mm]')
  plt.subplot(3,1,3)
  plt.
  plt.ylabel('COP [mm]')
  plt.xlabel('Time [s]')
  plt.pause(3)
  plt.savefig(fname+'_t-COP.png')
  plt.figure(2)
  L = 
  A = 
  plt.title('L={:.3E}[mm], Rect. A={:.3E}[mm^2]'.format(L,A))
  plt.xlabel('COPx [mm]')
  plt.ylabel('COPy [mm]')
  plt.pause(3)
  plt.

  df = pd.DataFrame(np.concatenate([X, COP], 1))
  df.to_excel(fname+'.xlsx',index=False,header=\
    ['Time', 'Fx', 'Fy', 'Fz', 'COPx', 'COPy','Mx','My','Mz','COP'])
# end of file