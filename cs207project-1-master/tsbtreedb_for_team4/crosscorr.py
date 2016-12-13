#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# CS207 Group Project Part 7
# Created by Team 2 (Jonne Seleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah) for Team 4

import os
import sys
import random
import numpy as np
import numpy.fft as nfft
from scipy.stats import norm

# This is a hacky solution to import the array time series class from sister directory by inserting it into system path
# should fix once time series library is turned into a proper python model

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.insert(0,d + '/timeseries')

import timeseries
import arraytimeseries as ats

def standardize(ts):
    """standardize timeseries ts by its mean and std deviation"""
    stand_vals = (ts.values() - ts.mean())/ts.std()
    return ats.ArrayTimeSeries(times=ts.times(), values=stand_vals)

def ccor(ts1, ts2):
    """
    given two standardized time series, compute their cross-correlation using FFT

    Args:
       ts1: first time series object
       ts2: second time series object
    Returns:
       Float - cross correlation value.

    Raises:
       ValueError: if length of ts1 and ts2 are not equal

    """

    # assert that len of ts1 = ts2
    if len(ts1) != len(ts2):
        raise ValueError("ts1 must be the same length as ts2 to calculate cross correlation")

    # fast fourier transform for ts1
    X = nfft.fft(ts1.values())

    # Complex conjugate of the fft transform of ts2
    Yhat = np.conjugate(nfft.fft(ts2.values()))

    # Normalizing scaler is required so that each shift is counted exactly once
    s = 1 / (1. * len(ts1))

    # The cross-correlation is the convolution of the fft transformed ts1 (X)
    # and the conjugate of ts2 (Yhat) scaled by s
    return  nfft.ifft(X * Yhat).real * s

def max_corr_at_phase(ts1, ts2):
    """ this is just for checking the max correlation with the kernelized cross-correlation """
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    maxcorr = ccorts[idx]
    return idx, maxcorr

def kernel_corr(ts1, ts2, mult=1):
    """
    Compute a kernelized correlation between two time series objects to be used as distance measure

    Args:
        ts1: first time series object. (Must be standardized.)
        ts2: second time series object. (Must be standardized.)
        m: multiplier factor. Defaults to 1. (Must be non-negative.)

    Returns:
        Float - kernelized correlation value

    The equation for the kernelized cross correlation is given at
    http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
    normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
    of a time series with itself is 1. We'll set the default multiplier to 1.
    """

    # calculate kernel
    # K(e^(m*ccor(ts1,ts2)))
    kernel = np.sum(np.exp(mult * ccor(ts1, ts2)))

    # Calculate kernel normalization constant:
    # sqrt(K(x,x)K(y,y))
    k_norm = np.sqrt(np.sum(np.exp(mult * ccor(ts1, ts1))) *
                     np.sum(np.exp(mult * ccor(ts2, ts2))))

    # return normalized kernel if k_norm is non-zero
    if k_norm != 0:
        return kernel/k_norm
    else:
        return 0

def kernel_dist(ts1, ts2, mult=1):
    """
    Calculates a cross-correlation based distance between two time series objects.

    Args:
        ts1: 1st time series object. (Must be standardized)
        ts2: 2nd time series object. (Must be standardized)
        m: multiplier factor. Defaults to 1. (Must be non-negative.)

    Returns:
        Float: distance value
    """

    # Ensure the time series have already been standardized
    if abs(ts1.mean()) >= .0001 or abs(ts2.mean()) >= .0001:
        raise ValueError("time series must be standardized before calculating kernel distance")

    # Calculate the kernel correlation value for ts1 and ts2
    kernel_corr_val = kernel_corr(ts1,ts2, mult)

    # Theorem 1-P4 in Pavlos paper states that the dist^2 = C(ts1,ts1)+C(ts2,ts2)-2C(ts1,ts2)
    # (Where C = kernel correlation )
    # However, we are using normalized kernels here, so the dist^2 will be 2(1-C(ts1,ts2))
    return np.sqrt(2*(1-kernel_corr_val))

def s_stats(n,ts):
    """Prints summary stats for ts """
    return "%s mean: %.4f, %s std: %.4f" % (n,ts.mean(),n,ts.std())
