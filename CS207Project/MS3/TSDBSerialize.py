import json
import sys
try:
	sys.path.append('../../MS1/'); from TimeSeries import TimeSeries 
except ImportError:
	sys.path.append('../MS1/'); from TimeSeries import TimeSeries 

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
		
	def json_to_bytes(self,json):
		"""
		Takes in JSON object, converts it to bytes
		"""
		return bytes(l, encoding='utf-8')

	# Note: Bytes to JSON is a two step process, first call bytes_to_json, then call load_json_dict to get JSON object
	def bytes_to_json(self,bytedata):
		"""
		Takes in bytes, converts it to JSON data
		"""
		return bytedata.decode('utf-8')

	def load_json_dict(self,jsondata):
		"""
		Takes in JSON data, and converts it to JSON object
		"""
		jsondict=json.loads(jsondata)
		return jsondict

	def jsondict_to_ts(self,jsondict):
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
