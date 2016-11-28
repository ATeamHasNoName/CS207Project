from numpy.fft import fft, ifft, fftshift
import numpy as np
#below is your module. Use your ListTimeSeries or ArrayTimeSeries..
import TimeSeries as ts
from scipy.stats import norm

def tsmaker(m, s, j):
    t = np.arange(0.0, 1.0, 0.01)
    #print(t)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return ts.TimeSeries(list(v), list(t))

def random_ts(a):
    t = np.arange(0.0, 1.0, 0.01)
    v = a*np.random.random(100)
    return ts.TimeSeries(list(v), list(t))

def stand(x, m, s):
    "standardize timeseries x my mean m and std deviation s"
    #your code here
    vals = np.array(list(x))
    vals = (vals - m)/s
    #return ts.TimeSeries(list(x.itertimes()),vals)
    return ts.TimeSeries(list(vals), list(x))


def ccor(ts1, ts2):
    "given two standardized time series, compute their cross-correlation using FFT"
    #your code here
    f1 = fft(list(ts1))
    f2 = fft(np.flipud(list(ts2)))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)



# this is just for checking the max correlation with the
#kernelized cross-correlation
def max_corr_at_phase(ts1, ts2):
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    maxcorr = ccorts[idx]
    return idx, maxcorr

#The equation for the kernelized cross correlation is given at
#http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
#normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
#of a time series with itself is 1. We'll set the default multiplier to 1.
def kernel_corr(ts1, ts2, mult=1):
    "compute a kernelized correlation so that we can get a real distance"
    #your code here.
    cross_cor = ccor(ts1, ts2)
    #temp
    temp = np.sum(np.exp(mult*cross_cor))
    return temp

#this is for a quick and dirty test of these functions
if __name__ == "__main__":
    print("HI")
    t1 = tsmaker(0.5, 0.1, 0.01)
    t2 = tsmaker(0.5, 0.1, 0.01)
    print(t1.mean(), t1.std(), t2.mean(), t2.std())
    import matplotlib.pyplot as plt
    plt.plot(t1)
    plt.plot(t2)
    plt.show()
    standts1 = stand(t1, t1.mean(), t1.std())
    standts2 = stand(t2, t2.mean(), t2.std())

    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts1, standts2, mult=10)
    print(sumcorr)
    t3 = random_ts(2)
    t4 = random_ts(3)
    plt.plot(t3)
    plt.plot(t4)
    plt.show()
    standts3 = stand(t3, t3.mean(), t3.std())
    standts4 = stand(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=10)
    print(sumcorr)
