# play_mocap.py
# usage: play_mocap.py v3dcsvfile p1 p2 p3 fpcsvfile 
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import 
import funcFilter

# 微分
def func_deriv(x, dt, Fc=10):
    nd = len(x)
    dx = np.zeros(nd)
    dx[1:] =
    Fs = 1/dt
    F = 
    y = 
    return y

# 3点角度
def func_angle_3points(pos1, pos2, pos3):
    nd = len(pos1[:,0])
    result = np.zeros(nd)
    for it in range(nd):
        va = 
        vb = 
        a = 
        b = 
        result[it] = 
    return result

# 最大値
def find_peak(x):
    xpeak = np.max(x)
    itpeak = 
    return itpeak, xpeak

if __name__=='__main__':
    args = sys.argv
    fname = args[1] #ポイントソート済c3dファイル(csv)
    t, x, y, z = 
    dt = np.mean(np.diff(t))
    nd = len(t)
    p_gretro_pos = int(args[2])-1
    p_a = int(args[3])-1
    p_b = int(args[4])-1
    p_c = int(args[5])-1

    fname_fp = args[6] #フォースプレートのデータファイル
    df = pd.read_csv('{}.csv'.format(fname_fp), header=8, names=\
    ('Time', 'Fx', 'Fy', 'Fz', 'COPx', 'COPy','Mx','My','Mz'))
    tfp = df['Time']
    Fx = df['Fx']
    Fy = df['Fy']
    Fz = df['Fz']

    exfname = 'res_{}-{}.png'.format(fname, fname_fp)

    pos_z = z[:,p_gretro_pos]
    pos_z = 
    itmax, zmax = 
    dat_a = np.concatenate(
        [x[:,p_a].reshape(nd,1), y[:,p_a].reshape(nd,1), z[:,p_a].reshape(nd,1)],1)
    dat_b = np.concatenate(
        [x[:,p_b].reshape(nd,1), y[:,p_b].reshape(nd,1), z[:,p_b].reshape(nd,1)],1)
    dat_c = np.concatenate(
        [x[:,p_c].reshape(nd,1), y[:,p_c].reshape(nd,1), z[:,p_c].reshape(nd,1)],1)
    x_angle = 
    v_angle = 
    a_angle = 

    plt.figure(figsize=[6,11])
    plt.
    plt.plot(t, pos_z, 'k-')
    plt.
    plt.plot([0, t[itmax]], [pos_z[itmax], pos_z[itmax]], 'c--')
    plt.text(t[itmax], pos_z[itmax], '{:.3f}'.format(pos_z[itmax]))
    plt.xlim(0, 2)
    plt.grid()
    plt.ylabel('z [m]')
    plt.subplot(5,1,2)
    plt.
    plt.xlim(0, 2)
    plt.grid()
    plt.ylabel('[deg]')
    plt.subplot(5,1,3)
    plt.plot(t, v_angle, 'k-')
    plt.xlim(0, 2)
    plt.grid()
    plt.ylabel('[deg/s]')
    plt.subplot(5,1,4)
    plt.plot(t, a_angle, 'k-')
    plt.xlim(0, 2)
    plt.grid()
    plt.ylabel('[deg/s^2]')
    plt.subplot(5,1,5)
    plt.plot(tfp, Fz, 'k-', label='Fz')
    plt.plot(tfp, Fx, color=[.8, .5, .5], label='Fx')
    plt.plot(tfp, Fy, color=[.5, .5, .8], label='Fy')
    plt.ylabel('F [N]')
    plt.xlabel('Time [s]')
    plt.grid()
    plt.legend()
    plt.xlim(0, 2)
    plt.
    plt.
# end of file