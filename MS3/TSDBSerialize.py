import json
import sys
sys.path.append('../MS1/')
from TimeSeries import TimeSeries 

#create dummy time series
t = [1.5, 2, 2.5, 3, 10.5]
v = [1, 3, 0, 1.5, 1]
z = TimeSeries(values=v, times=t)
print("The input time series times are ", t)
print("The input time series values are ", v)

class Serialize:
	def ts_to_json(self,ts):
	    times=ts.times()
	    vals=ts.values()
	    lst=[]
	    for i in range(len(vals)):
	        lst.append((times[i],vals[i]))
	        rs = json.dumps(dict(lst))
	    return rs
	    
	def json_to_bytes(self,json):
		return bytes(l, encoding='utf-8')

	def bytes_to_json(self,bytedata):
		return bytedata.decode('utf-8')

	def load_json_dict(self,jsondata):
		jsondict=json.loads(jsondata)
		return jsondict

	def jsondict_to_ts(self,jsondict):
		treconstruct=[]
		vreconstruct=[]
		for key in jsondict.keys():
		    treconstruct.append(float(key))
		    vreconstruct.append(float(jsondict[key]))
		tsreconstruct=TimeSeries(values=vreconstruct,times=treconstruct)
		return tsreconstruct

a=Serialize()

l=a.ts_to_json(z)
print(l)

#convert ts to bytes
k=a.json_to_bytes(l)


##### deconding begins ######

#convert bytes to json
j=a.bytes_to_json(k)


#Load json as dictionary
i=a.load_json_dict(j)

#reconstruct time series object from dictionary - 
reconstructed_timeseries=a.jsondict_to_ts(i)

print("The reconstructed time series' times are ",reconstructed_timeseries.timesseq)
print("The reconstructed time series' values are ",reconstructed_timeseries.valuesseq)
