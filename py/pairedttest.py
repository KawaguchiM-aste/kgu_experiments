# pairedttest.py
# usage: python pairedttest.py 
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import datetime

alpha = 0.05
ylabel = 'L[mm]'
Cond=['X','Y']
X=np.array([10.01, 4.75, 2.63, 2.45, 6.69, 3.73, 18.9, 9.93, 5.97, 10.26, 12.17, 10.46])
Y=np.array([3.95, 2.15, 1.1, 0.26, 6.28, 12.78, 5.62, 3.98, 2.42, 3.72, 7.02, 7.911])

class trel:
  def drawttestbox(self,x,y):
    vx=np.array([1,2])
    vy=np.array([np.mean(x), np.mean(y)])
    sy=np.array([np.std(x), np.std(y)])
    X=x.reshape(len(x),1)
    Y=y.reshape(len(y),1)
    Z=np.concatenate([X,Y],1)
    plt.boxplot(Z,labels=Cond,showmeans=True)
    for i in range(len(x)):
      plt.plot([1,2],[x[i],y[i]],'co-',alpha=0.2)
    plt.ylabel(ylabel)
    tstat=stats.ttest_rel(x,y)
    p = tstat.pvalue
    t = tstat.statistic
    df = len(x)-1
    d = np.abs(np.mean(X-Y))/np.std(X-Y)
    str = 't({})={:.3f}, p={:.3f}'.format(df,t,p)
    print('Average: {:.3E}, {:.3E}'.format(vy[0],vy[1]))
    print('SD     : {:.3E}, {:.3E}'.format(sy[0],sy[1]))
    print(str)
    m=np.max(vy)+1.5*np.max(sy)
    mt=np.max(vy)+1.6*np.max(sy)
    if p<alpha:
      plt.plot([1.1,1.9],[m,m],'k')
      plt.text(1.5,mt,'p<{}'.format(alpha))
    return t,p,df

if __name__=='__main__':
  ttest=trel()
  ttest.drawttestbox(X,Y)
  now=datetime.datetime.now()
  exfname=now.strftime('%Y%m%d%H%M%S')
  exfname='{}_pairedttest_{}_{}-{}.png'.format(exfname,ylabel,Cond[0],Cond[1])
  #plt.show()
  plt.pause(3)
  plt.savefig(exfname)
# end of file