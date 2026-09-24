# play_mocap.py
# usage: play_mocap.py csvfilename
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import sys
import os
import glob
from PIL import Image

# 欠損値を置換
def func_elimlett(x):
    N = x.shape[1]
    nd = x.shape[0]
    y = np.zeros((nd,N))
    for it in range(nd):
        for j in range(N):
            if x[it][j] == '*':
                y[it][j] = 0
            else:
                y[it][j] = x[it][j]
    return y

# アニメーション
def drawAnime(pos_x, pos_y, pos_z, dt=1/30, StickPic=None, exfname='result'):
    nd = len(pos_x[:,0])
    ax = plt.figure().add_subplot(projection='3d')
    Nmarkers = pos_x.shape[1]
    min_pos = np.min([np.min(pos_x), np.min(pos_y), np.min(pos_z)])
    max_pos = np.max([np.max(pos_x), np.max(pos_y), np.max(pos_z)])

    gifpath = 'temp'
    if not os.path.isdir(gifpath):
        os.makedirs(gifpath)

    if StickPic is not None:
        ind = np.where(StickPic>0)
        i1 = ind[0]
        i2 = ind[1]
        nline = len(ind[0])
    
    for it in range(nd):
        ax.cla()
        ax.plot(pos_x[it,:], pos_y[it,:], pos_z[it,:], 'o')
        plt.title('{}Markers, {:.3f}[s]'.format(Nmarkers, it*dt))
        for i in range(Nmarkers):
            ax.text(pos_x[it,i], pos_y[it,i], pos_z[it,i], '{}'.format(i+1))
        if StickPic is not None:
            for i in range(nline):
                v = [i1[i], i2[i]]
                ax.plot(pos_x[it,v], pos_y[it,v], pos_z[it,v])
        ax.set_xlim(min_pos, max_pos)
        ax.set_ylim(min_pos, max_pos)
        ax.set_zlim(min_pos, max_pos)
        plt.xlabel('Axes-X')
        plt.ylabel('Axes-Y')
        plt.pause(dt)
        plt.savefig('{}/{:0=5}.png'.format(gifpath, it))
    
    print('[Exporting] Animation...')
    picList = sorted(glob.glob(gifpath+'/*.png'))
    fig = plt.figure()
    frame = []
    for it in range(len(picList)):
        tmp = Image.open(picList[it])
        frame.append([plt.imshow(tmp)])
    anime = animation.ArtistAnimation(fig,frame,interval=dt*1000)
    anime.save(exfname+'.gif')
    for rmfile in picList:
        os.remove(rmfile)
    os.rmdir(gifpath)
    print('[Exported] {}.gif'.format(exfname))

def read_v3dcsv(fname):
    print('... Loading {}'.format(fname))
    df = pd.read_csv('{}.csv'.format(fname),header=16)

    t = df.iloc[:,2]
    datpos = df.iloc[:,3:]
    nd = len(t)
    Npos = int(datpos.shape[1]/3)
    datpos = datpos.values.reshape(nd,datpos.shape[1])
    datpos_rev = func_elimlett(datpos)
    pos_x = np.zeros((nd,Npos))
    pos_y = np.zeros((nd,Npos))
    pos_z = np.zeros((nd,Npos))
    for i in range(Npos):
        ii = i*3
        pos_x[:,i]=datpos_rev[:,ii]
        pos_y[:,i]=datpos_rev[:,ii+1]
        pos_z[:,i]=datpos_rev[:,ii+2]
    return t, pos_x, pos_y, pos_z

if __name__=='__main__':
    args = sys.argv
    fname = args[1] #ポイントソート済c3dファイル(csv)
    t, pos_x, pos_y, pos_z = read_v3dcsv(fname)
    dt = np.mean(np.diff(t))

    # まずアニメーションを見て，マーカー番号とその位置を確認する
    drawAnime(pos_x, pos_y, pos_z, dt)

    # スティックピクチャ行列
    #Mstick = np.array(
    #        [[0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 1, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0],
    #         [0, 1, 0, 0, 0, 1, 0],
    #         [0, 0, 1, 0, 0, 0, 1],
    #         [0, 0, 0, 1, 0, 0, 1],
    #         [0, 0, 0, 0, 1, 1, 0]])
    #drawAnime(pos_x, pos_y, pos_z, dt, Mstick, fname)
#end of file