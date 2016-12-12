from scipy.stats import norm
import random
import os
import numpy as np
import sys
sys.path.append('../timeseries')
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries
from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface
sys.path.append('../cs207rbtree')
import redblackDB
sys.path.append('../SimSearch')
from _corr import kernel_dist

# py.test --doctest-modules  --cov --cov-report term-missing Distance_from_known_ts.py

def load_ts_file(filepath):
    '''
    Takes in file and reads time series from it

	Parameters
	----------
	filepath: path of the file 
	
	Returns
	-------
	timeSeries object : TimeSeries class

	>>> ts=load_ts_file('169975.dat_folded.txt')

	>>> ts._values[0]
	15.137
    '''
#Only considers the first two columns of the text file (other columns are discarded)
#Only evaluates time values between 0 and 1
#First column is presumed to be times and second column is presumed to be light curve values.
    data = np.loadtxt(filepath, delimiter=' ',dtype = str)
    clean_input = []
    for i in range(len(data)):
        row = data[i].split("\\t")
        clean_input.append([float(row[0][2:]),float(row[1])])
    data = np.array(clean_input)

    _ , indices = np.unique(data[:, 0], return_index=True)

    data = data[indices, :]
    times, values = data.T
    full_ts = TimeSeries(times=list(times),values=list(values))
    interpolated_ts = full_ts.interpolate(list(np.arange(0.0, 1.0, (1.0 /100))))
    full_ts_interpolated = TimeSeries(times=list(np.arange(0.0, 1.0, (1.0 /100))),values=list(interpolated_ts))
    return full_ts_interpolated

if len(sys.argv)<2:
	raise ValueError("No input file containing time series passed")
else:
	test_ts=load_ts_file(sys.argv[1])

num_vantage_points = 5
num_of_timeseries = 30
num_top=int(sys.argv[2])

def tsmaker(m, s, j):
    '''
    Creates a random time series of 100 elements

	Parameters
	----------
	m,s,j: parameters of the function norm.pdf

	Returns
	-------
	timeSeries object : TimeSeries class

	>>> ts = tsmaker(2,3,4)

	>>> ts._times[0]
	0.0
    '''
    t = list(np.arange(0.0, 1.0, 0.01))
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return TimeSeries(values=v,times=t)

#[{1: <dist>, 2: <dist>, }_1, {}_2, ... {}_20] to
# (1,2);(2,3)....|(3,4);.....|
def encodeVantagePoints(decoded):
	'''
	Encodes the vantage point to a string so that it can be stored

	Parameters
	----------
	Decoded: Any list that is to be encoded

	Returns
	-------
	string

	>>> ts=encodeVantagePoints({1:(1,2)})
	>>> ts[1]
	'1'
	'''
	# dbstring = []
	# for distances in decoded:
	distancestring = []
	for k, v in decoded.items():
		distancestring.append("(" + str(k) + "," + str(v) + ")")
	encodedString = ';'.join(distancestring)
	return encodedString
	# dbstring.append(';'.join(distancestring))
	# return '|'.join(dbstring)

# (1,2);(2,3)....|(3,4);.....| to
#[{1: <dist>, 2: <dist>, }_1, {}_2, ... {}_20]
def decodeVantagePoints(encoded):
	'''
	>>> ts=decodeVantagePoints('(1,2);(2,3)')
	>>> ts
	{1: 2.0, 2: 3.0}
	'''
	dict_distances = {}
	items = encoded.split(';')
	for item in items:
		# Grab key and value
		split = item.split(',')
		key = int(split[0][1:])
		value = float(split[1][:-1])
		dict_distances[key] = value
	return dict_distances

def encodeTimeSeries(timeSeries):
	"""
	Takes in time series object and transforms it into a string.
	
	Parameters
	----------
	timeSeries: Concrete class of SizedContainerTimeSeriesInterface
	
	Returns
	-------
	String representation of time series object, where each time and value is encoded in 
	"(t,v)" and separated with ";"

	>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
	>>> k=encodeTimeSeries(ts)
	>>> k
	'(1,0);(1.5,2);(2,-1);(2.5,0.5);(10,0)'
	"""
	items = timeSeries.items()
	encodedTimeSeries = []
	for (time, value) in items:
		encodedTimeSeries.append("(" + str(time) + "," + str(value) + ")")
	return ';'.join(encodedTimeSeries)

# Takes in encoded time series and transforms it into a TimeSeries object
# Raise ValueError whenever improper
def decodeTimeSeries(encodedTimeSeries):
	"""
	Takes in time series string and transforms it into a time series object.
	Raises ValueError when the input string is malformed.
	
	Parameters
	----------
	String representation of time series object, where each time and value is encoded in 
	"(t,v)" and separated with ";"
	
	Returns
	-------
	timeSeries: TimeSeries class

	>>> ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
	>>> encodedString = encodeTimeSeries(ts)
	>>> k=decodeTimeSeries(encodedString)
	>>> k
	TimeSeries(Length: 5, [0.0, 2.0, -1.0, 0.5, 0.0])
	"""
	itemStrings = encodedTimeSeries.split(';')
	t = []
	v = []
	for itemString in itemStrings:
		timeValuePair = itemString.split(',')

		if len(timeValuePair) != 2:
			raise ValueError('Time series string is malformed')

		time = timeValuePair[0]
		value = timeValuePair[1]
		if len(time) < 2 or len(value) < 2:
			raise ValueError('Time series string is malformed')			
		
		time = time[1:]
		value = value[:-1]

		# This might throw ValueError if time and value could not be converted to floats
		t.append(float(time))
		v.append(float(value))

	z = TimeSeries(values=v, times=t)
	return z

def write_ts(ts,i):
    """ Write light curve to disk as space delimited text file"""
    '''
    Write light curve to disk as space delimited text file
	
	Parameters
	----------
	ts: time series object
	i : a counter to be appended to the file name where it is stored 
	Returns
	-------
	None. 
    '''
    path = "ts-{}.txt".format(i)
    datafile_id = open(path, 'wb')
    data = np.array([ts._times, ts._values])
    data = data.T

    np.savetxt(datafile_id, data, fmt=['%.3f','%8f'])
    datafile_id.close()

 # Get distance from vantage points from DB, and if its not there then proceed

db = redblackDB.connect("distanceFromVantagePoints.dbdb")
db_vantagepoints = redblackDB.connect("vantagePoints.dbdb")
db_data = redblackDB.connect("timeseriesdata.dbdb")

distances_from_vantage_points = []
v=[]
x=[]

try:

	for i in range(num_vantage_points):
		key='v'+str(i)
		decodedVantagePoints=db_vantagepoints.get(key)
		v.append(decodeTimeSeries(decodedVantagePoints))
		distances_from_vantage_points.append(decodeVantagePoints(db.get(key)))

	for i in range(num_of_timeseries):
		key='x' + str(i)
		x.append(decodeTimeSeries(db_data.get(key)))

except KeyError:
	
	# Calculate and cache on disk
	print('Not stored in disk, calculate distances')

	#generation of 1000 time series
	for i in range(num_of_timeseries):
		ts=tsmaker(4,2,8)
		x.append(ts)
		db_data.set('x' + str(i), encodeTimeSeries(ts))
	db_data.commit()

	#generate 20 vantage points 
	indices = random.sample(range(num_of_timeseries), num_vantage_points)
	for i in range(0,num_vantage_points):
		vi = x[indices[i]]
		dbKey_vantagepoint='v'+str(i)
		db_vantagepoints.set(dbKey_vantagepoint,encodeTimeSeries(vi))
		v.append(vi)
	db_vantagepoints.commit()

	#Find distance of all points from each vantage point, store in array of dictionaries.
	for i in range(num_vantage_points):
		print('Working on vantage point: ', i)
		dict_distances = {}
		for j in range(num_of_timeseries):
			distance_bw=kernel_dist(v[i],x[j])
			dict_distances[j]=distance_bw
		distances_from_vantage_points.append(dict_distances)
		db.set('v' + str(i), encodeVantagePoints(dict_distances))
	db.commit()

corr=0
closest='dummy'

#Find closest vantage point
for i in range(num_vantage_points):
	if kernel_dist(test_ts,v[i]) > corr:
		corr = kernel_dist(test_ts,v[i])
		closest = str(i)

#Define region between them
max_region=2*corr
remaining_time_series=[];

distances_from_closest = decodeVantagePoints(db.get('v' + closest))

for index in distances_from_closest.keys():
	distance=distances_from_closest[index]
	if distance > max_region:
		del distances_from_closest[index]

final_distances = []

#find top-n-cut in this
for i in distances_from_closest.keys():
	distance_from_test_sample=kernel_dist(x[i],test_ts)
	final_distances.append((i,distance_from_test_sample))
final_distances.sort(key=lambda x:x[1])

# final_distances
indexes_and_distances_of_top_20=final_distances[:num_top]
print("\nThe indexes and distances of top 20 matches are \n\n",indexes_and_distances_of_top_20)

counter=0
for (key_top, _) in indexes_and_distances_of_top_20:
	ts_top = decodeTimeSeries(db_data.get('x'+str(key_top)))
	print(ts_top)
	write_ts(ts_top,counter)
	counter+=1
print("The files have been written in the directory!")