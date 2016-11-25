from scipy.stats import norm
import random
import numpy as np
from WrappedDB import WrappedDB
import sys
sys.path.append('../')
from TimeSeries import TimeSeries
db=[];
tsobj=[];
x=[];
v=[];
#db1=WrappedDB("exampleDB.dbdb")
def tsmaker(m, s, j):
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return TimeSeries(t, v)

#generation of 1000 time series
for i in range(0,1000):
	ts=tsmaker(5,1,4)
	vals=ts.values()
	x.append(vals)

#generate 20 vantage points 
indices=random.sample(range(0,1000),20)
for i in range(0,20):
	v.append(x[indices[i]])
