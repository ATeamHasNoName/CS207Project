import numpy.fft as nfft
import sys   
import numpy as np
from scipy.stats import norm
sys.path.append("../timeseries/")
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries



def stand(ts):
    '''
    Standardizes timeseries using its mean m and its standard 
    '''
    # stand = (ts._values() - ts.mean())/ts.std()
    arrayvalues = np.asarray(ts._values)
    stand =  (arrayvalues - ts.mean()) / ts.std()
    # print("ts values were ",ts._values)
    # print("I standardized them to",stand)
    # print("using ",ts.mean(),ts.std())
    return TimeSeries(times=ts._times, values=stand)


def ccor(ts1, ts2):
    '''
    Given two standardized time series, computes their cross-correlation using
    fast fourier transform. Assume that the two time series are of the same
    length.
    Parameters
    ----------
    ts1 : TimeSeries
        A standardized time series
    ts2 : TimeSeries
        Another standardized time series
    Returns
    -------
    The two time series' cross-correlation.
    '''
    # calculate fast fourier transform of the two time series
    stand1=stand(ts1)
    stand2=stand(ts2)
    fft_ts1 = nfft.fft(stand1._values)
    fft_ts2 = nfft.fft(stand2._values)

    # print(len(ts1))
    # print(len(ts2))
    # assert len(ts1) == len(ts2)

    # return cross-correlation, i.e. the convolution of the first fft
    # and the conjugate of the second
    return ((1 / (1. * len(ts1))) *
            nfft.ifft(fft_ts1 * np.conjugate(fft_ts2)).real)


def max_corr_at_phase(ts1, ts2):
    '''
    Given two standardized time series, determines the time at which their
    cross-correlation is maximized, as well as the cross-correlation itself
    at that point.
    Parameters
    ----------
    ts1 : TimeSeries
        A standardized time series
    ts2 : TimeSeries
        Another standardized time series
    Returns
    -------
    idx, maxcorr : int, float
        Tuple of the time at which cross-correlation is maximized, and the
        cross-correlation at that point.
    '''

    # calculate cross-correlation between the two time series
    ccorts = ccor(ts1, ts2)

    # determine the time at which cross-correlation is maximized
    idx = np.argmax(ccorts)

    # determine the value of cross-correlation at that time
    maxcorr = ccorts[idx]

    # return the time, cross-correlation tuple
    return idx, maxcorr


def kernel_corr(ts1, ts2, mult=1):
    '''
    Given two standardized time series, calculates the distance between them
    based on the kernelized cross-correlation. The kernel is normalized so that
    the cross-correlation of a time series with itself equals one.
    Reference: http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
    Parameters
    ----------
    ts1 : TimeSeries
        A standardized time series
    ts2 : TimeSeries
        Another standardized time series
    mult : int
        Multiplicative constant in kernel function (gamma)
    Returns
    -------
    float
        Distance between two time series.
    '''

    # calculate cross-correlation
    cross_correlation = ccor(ts1, ts2)

    # calculate kernel
    num = np.sum(np.exp(mult * cross_correlation))

    # calculate kernel normalization
    denom = np.sqrt(np.sum(np.exp(mult * ccor(ts1, ts1))) *
                    np.sum(np.exp(mult * ccor(ts2, ts2))))

    # return normalized kernel
    if denom == 0:
        return 0
    else:
        return num/denom

def kernel_dist(ts1, ts2, mult=1):
    '''
    Given two standardized time series, calculates the distance between them
    based on the kernelized cross-correlation.
    ----------
    ts1 : TimeSeries
        A standardized time series
    ts2 : TimeSeries
        Another standardized time series
    mult : int
        Multiplicative constant in kernel function
    Returns
    -------
    float
        Distance value
    '''
    stand1=stand(ts1)
    stand2=stand(ts2)

     # Ensure the time series have already been standardized
    if abs(stand1.mean()) >= .001 or abs(stand2.mean()) >= .001:
        # print("hello")
        #print("ts1 mean is ",ts1.mean(),"ts2 mean is ",ts2.mean())
        raise ValueError("Time series must be standardized")

    # The kernel correlation value for ts1 and ts2
    kernel_corr_val = kernel_corr(ts1,ts2, mult)

    # dist= sqrt(C(ts1,ts1)+C(ts2,ts2)-2C(ts1,ts2))
    # When using normalized kernels, dist = sqrt(2(1-C(ts1,ts2)))
    return np.sqrt(2*(1-kernel_corr_val))

