# usage: python ana_mocap_ave.py <file1> <file2> <file3>
# e.g. : python ana_mocap_ave.py hoge1 hoge2 hoge3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys

if __name__=='__main__':
    args = sys.argv
    nfiles = len(args)-1
    c = np.linspace(0, 1, nfiles)
    nds = np.zeros(nfiles)
    # ファイルの読込
    for i in range(nfiles):
        fname = args[i+1]
        print('... Loading {}.xlsx'.format(fname))
        dat = pd.read_excel('{}.xlsx'.format(fname),header=0)
        h = dat.columns
        n = len(h)-1 
        t = dat[h[0]]
        nds[i] = len(t)
        nd = len(t)
        for j in range(n):
            plt.figure(j+1)
            plt.plot(t, dat[h[j+1]], color=[c[i], 0, 1-c[i]])
            if i==0:
                plt.ylabel(h[j+1])
    # 描画(1回ずつ)
    for j in range(n):
        plt.figure(j+1)
        plt.xlabel('Time')
        plt.pause(1)
        plt.savefig('ave_{}_{}.png'.format(fname[:10],h[j+1][:5]))
        print('[Exported] ave_{}_{}.png'.format(fname[:10],h[j+1][:5]))
        plt.close(j+1)
    # 時刻が正規化されている場合，以下を実行
    if np.all(np.diff(nds) == 0):
        print('This is normalized...')
        Z = np.zeros((nd, nfiles+2, n))
        hh = [0]
        # 初回のデータを保持していないので，再度ファイルの読込
        for i in range(nfiles):
            hh.append(i+1)
            fname = args[i+1]
            print('... Loading {}.xlsx'.format(fname))
            dat = pd.read_excel('{}.xlsx'.format(fname),header=0)
            for j in range(n):
                Z[:, i, j] = dat[h[j+1]]
        hh.append('Average')
        hh.append('SD')
        hh = hh[1:]
        for j in range(n):
            exfname = 'avenorm_{}_{}'.format(fname[:10],h[j+1][:5])
            for it in range(nd):
                # 平均とSDの算出
                Z[it, nfiles, j] = np.nanmean(Z[it, :-2, j])
                Z[it, nfiles+1, j] = np.nanstd(Z[it, :-2, j])
            # 描画(SDをエラーバーで表現)
            plt.figure(j+1)
            plt.errorbar(t, Z[:,nfiles,j],yerr=Z[:,nfiles+1,j],ecolor='c')
            plt.plot(t, Z[:,nfiles,j], 'k-')
            plt.ylabel(h[j+1])
            plt.xlabel('Normalized Time [%]')
            plt.pause(1)
            plt.savefig('{}.png'.format(exfname))
            print('[Exported] {}.png'.format(exfname))
            # Excelファイルに出力
            df = pd.DataFrame(Z[:,:,j])
            if j==0:
                with pd.ExcelWriter('avenorm_{}.xlsx'.format(fname[:10]), engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=h[j+1][:2], index=False, header=hh)
            else:
                with pd.ExcelWriter('avenorm_{}.xlsx'.format(fname[:10]), engine='openpyxl',mode='a') as writer:
                    df.to_excel(writer, sheet_name=h[j+1][:2], index=False, header=hh)
        print('[Exported] avenorm_{}.xlsx'.format(fname[:10]))
#end of file