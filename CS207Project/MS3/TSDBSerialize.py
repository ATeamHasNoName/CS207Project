import json
import sys
import os
try:
	sys.path.append(os.path.abspath('../../MS1/')); from TimeSeries import TimeSeries 
except ImportError:
	sys.path.append(os.path.abspath('../MS1/')); from TimeSeries import TimeSeries 

class Serialize:
	"""
	Serialize class that does conversions between TimeSeries, JSON and Bytes.
	"""
	def ts_to_json(self,ts):
		"""
		Takes in TimeSeries, converts it to JSON object
		"""
		times=ts.times()
		vals=ts.values()
		lst=[]
		for i in range(len(vals)):
			lst.append((times[i],vals[i]))
			rs = json.dumps(dict(lst))
		# Convert JSON string to JSON object
		return json.loads(rs)

	def json_to_ts(self,jsondict):
		"""
		Takes in JSON object, and converts it into TimeSeries
		"""
		treconstruct=[]
		vreconstruct=[]
		for key in jsondict.keys():
			treconstruct.append(float(key))
			vreconstruct.append(float(jsondict[key]))
		tsreconstruct=TimeSeries(values=vreconstruct,times=treconstruct)
		return tsreconstruct
		
	def json_to_bytes(self,jsondict):
		"""
		Takes in JSON object, converts it to bytes
		"""
		# Need to first convert jsondict to json string
		return bytes(json.dumps(jsondict), encoding='utf-8')

	def bytes_to_json(self,bytedata):
		"""
		Takes in bytes, converts it to JSON object
		"""
		return json.loads(bytedata.decode('utf-8'))

