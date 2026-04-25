# exportOpenSignals.py
# usage: python exportOpenSignals.py <txt file>
# e.g. : python exportOpenSignals.py opensignals20XX.txt

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import json
from opensignalsreader import OpenSignalsReader

args = sys.argv
fname=args[1]
print('... Loading {}'.format(args[1]))
acq = OpenSignalsReader(fname, show=True)
dat = acq.signal()
with open(fname) as f:
  txtmeta=f.readlines()[1]
jsonmeta=json.loads(txtmeta[1:])
Binalino_ID=txtmeta[4:21]
Fs = int(jsonmeta[Binalino_ID]['sampling rate'])
print('Sampling Frequency: {}Hz'.format(Fs))
dt = 1/Fs
for sensType in dat.keys():
  tmp = dat[sensType]
  nd = len(tmp)
  t = np.linspace(dt,dt*nd,nd)
  t = t.reshape(nd,1)
  x = tmp.reshape(nd,1)
  exfname='{}_{}.xlsx'.format(fname[:-4],sensType)
  df = pd.DataFrame(np.concatenate([t, x], 1))
  df.to_excel(exfname,index=False,header=None,sheet_name='raw')
  print('Exported: {}'.format(exfname))
# end of file