import os, sys
import TimeSeries as ts
import SimilaritySearch as ss
import numpy as np
import random
import btreeDB


if __name__ == "__main__":

    file_name = "ts_data_6.txt"
    ts_data = np.loadtxt(file_name, delimiter=' ')
    comp_ts = ts.TimeSeries(ts_data[:, 1], ts_data[:, 0])
    std_comp_ts = ss.stand(comp_ts, comp_ts.mean(), comp_ts.std())

    #to be continue..
    #how to find the nearest k nodes?
