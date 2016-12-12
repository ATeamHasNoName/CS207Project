import json
import sys
sys.path.append('../MS1/')
from TimeSeries import TimeSeries 

#create dummy time series
t = [1.5, 2, 2.5, 3, 10.5]
v = [1, 3, 0, 1.5, 1]
z = TimeSeries(v, t)
print("The input time series times are ", t)
print("The input time series values are ", v)
def ts_to_json(ts):
    times=ts.times()
    vals=ts.values()
    lst=[]
    for i in range(len(vals)):
        lst.append((times[i],vals[i]))
        rs = json.dumps(dict(lst))
    return rs
    
l=ts_to_json(z)


#convert ts to bytes
k=bytes(l, encoding='utf-8')


##### deconding begins ######

#convert bytes to json
l=k.decode('utf-8')


#Load json as dictionary
h=json.loads(l)

#reconstruct time series object from dictionary - 
def jsondict_to_ts(jsondict):
	treconstruct=[]
	vreconstruct=[]
	for key in h.keys():
	    treconstruct.append(float(key))
	    vreconstruct.append(float(h[key]))
	tsreconstruct=TimeSeries(values=vreconstruct,times=treconstruct)
	return tsreconstruct

reconstructed_timeseries=jsondict_to_ts(h)
print("The reconstructed time series' times are ",reconstructed_timeseries.timesseq)
print("The reconstructed time series' values are ",reconstructed_timeseries.valuesseq)
