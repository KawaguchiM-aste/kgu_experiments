# usage: python ana_mocap_normalize.py <data file>
# e.g. : python ana_mocap_normalize.py hoge
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys

def func_tnorm(ve, itmin, itnorm):
    # ve: 正規化したい物理量
    # itmin: 参照点の時刻インデックス(何行目)
    # itinorm: itminを何%とするか
    te = np.zeros(len(ve))
    for i in range(len(itmin)-1):
        te[itmin[i]:itmin[i+1]+1] = np.linspace(itnorm[i], itnorm[i+1], len(te[itmin[i]:itmin[i+1]+1]))
    nd = itmin[i+1]+1
    i_start = itmin[0]
    #  他データと比較可能なように長さ(間隔)を固定する
    dtn = 1.0
    tnew = np.arange(0, np.max(te)+dtn, dtn)
    vnew = np.interp(tnew, te[i_start:nd], ve[i_start:nd])
    return vnew, tnew

if __name__=='__main__':
    # ファイルの読込
    args = sys.argv
    fname = args[1] #ファイル名の共通部分
    fname_kine = 'res_{}.xlsx'.format(fname)
    fname_time = 'timings_{}.xlsx'.format(fname)
    print('... Loading {}'.format(fname_kine))
    dat = pd.read_excel(fname_kine,header=0)
    print('... Loading {}'.format(fname_time))
    datt = pd.read_excel(fname_time,header=0)

    # 項目名(列の名前)の取得
    itnorm = datt['normalizedtime']
    tref = datt['time']
    itref = np.zeros(len(itnorm), dtype=int)
    header = dat.columns
    n = len(header)
    t = dat[header[0]]

    # 正規化の基準とする時刻インデックスの取得
    for i in range(len(itref)):
        for it in range(len(t)-1):
            if t[it]<=tref[i] and t[it+1]>tref[i]:
                itref[i] = it
    
    # 正規化と描画
    exfname = 'nt_{}'.format(fname)
    for i in range(len(header)):
        x, t_new = func_tnorm(dat[header[i]], itref, itnorm) #ここで正規化
        if i==0:    
            nd = len(t_new)
            Z = np.zeros((nd,n))
            Z[:,0] = t_new   
        else:
            Z[:,i] = x
            plt.figure()
            plt.subplot(2,1,1)
            plt.plot(t, dat[header[i]])
            plt.xlabel('Time [s]')
            plt.ylabel(header[i])
            plt.subplot(2,1,2)
            plt.plot(t_new, x)
            plt.xlabel('Normalized Time [%]')
            plt.ylabel(header[i])
            plt.pause(1)
            plt.savefig('{}_{}.png'.format(exfname,header[i][:5]))
            print('[Exported] {}_{}.png'.format(exfname,header[i][:5]))

    # ファイルの出力
    df = pd.DataFrame(Z)
    with pd.ExcelWriter('{}.xlsx'.format(exfname), engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=header)
    print('[Exported] {}.xlsx'.format(exfname))
# end of file