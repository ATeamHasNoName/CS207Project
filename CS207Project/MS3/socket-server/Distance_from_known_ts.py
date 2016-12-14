from scipy.stats import norm
import random
import os
import numpy as np
import sys
from _corr import kernel_dist
import requests
import pprint
sys.path.append('../../MS1')
from TimeSeries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
sys.path.append('../../MS2')
from FileStorageManager import FileStorageManager
from DB import *

def FindTimeSeriesByKey(key):
	"""
	Gets the time series object in FSM from its key. This is being called by /timeseries/<id> GET.
	"""
	fsm = FileStorageManager()
	ts = fsm.get(key)
	return ts

# py.test --doctest-modules  --cov --cov-report term-missing Distance_from_known_ts.py
def Simsearch(inputTS, k, id_or_ts):
	num_vantage_points = 20 # NOTE: Remember to change this number in flaskr.py too!
	num_of_timeseries = 1000
	num_top = k
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

	# Check if we have cached by verifying the existence of this file
	vantage_index_file_name = "db_vantageindex.dbdb"
	fsm = FileStorageManager()

	# Initialization code to generate 1000 TimeSeries, sample 20 vantage points, and store all of them in the right places
	try:
		vantageDB = DB.connect(vantage_index_file_name)
		vantageDB.get("0")
		#print("Vantage points already initialized")
		
	except KeyError:
		# Have to delete file that is created in the try block above or this will cause the connect in Step 2 to crash
		DB.remove(vantage_index_file_name)
		
		print('Not stored in disk, calculate distances')

		# 1000 TimeSeries IDs in memory that will be populated by Step 1
		all1000IDs = []
		# Step 1: Generation of 1000 time series
		for i in range(num_of_timeseries):
			ts=tsmaker(4,2,8)

			# Store this time series in FSM
			tsID = fsm.store(timeSeries = ts)

			# Send the time series over to API Server to update metadata
			# First convert time series object to time series JSON
			timeseriesJSON = {}
			for (time_, value_) in ts.items():
				timeseriesJSON[str(time_)] = value_

			APIServer = 'http://{}:{}/generatemetadata'.format("localhost", 5001)
			response = requests.post(APIServer, json={'id': tsID, 'timeseries': timeseriesJSON})
			if response.status_code not in [200, 201]:
				raise ValueError('Failed to store one out of 1000 time series metadata in PostgreSQL')

			# Append the ID to the list and keep going
			all1000IDs.append(str(tsID))

		# Step 2: Generate 20 random indices as vantage point id's, and store them in a .txt file as an Index
		vantage_point_indexes = random.sample(range(num_of_timeseries), num_vantage_points)
		vantageIndexDB = DB.connect(vantage_index_file_name)
		vantageLabel = 0
		for i in vantage_point_indexes:
			vantageID = all1000IDs[i]
			vantageIndexDB.set(str(vantageLabel), vantageID)
			vantageLabel += 1
		vantageIndexDB.commit()

		# Step 3: Generate 20 red black trees, each containing 1000 nodes of distances to vantage point
		# Filename will be db_vantagepoint_<vantageid>
		for i in vantage_point_indexes:
			# For each vantage point do the following:

			vantageID = all1000IDs[i]
			print('Working on vantage point with id: ', vantageID)

			vantage_file_name='db_vantagepoint_'+ vantageID + '.dbdb'
			vantageDB=DB.connect(vantage_file_name)
			vantageTS = fsm.get(vantageID)

			for j in range(num_of_timeseries):
				# For each timeseries, calculate the distance to this vantage point and append it to RBT: 

				otherID = all1000IDs[j]
				otherTS = fsm.get(otherID)
				distance_bw = kernel_dist(otherTS, vantageTS)
				vantageDB.set(str(distance_bw), otherID)

			# Note: We commit after setting all 1000 distances so we make it more efficient
			vantageDB.commit()	

		# Step 4: Store indexes of the 1000 Time series generated so we can reference them later
		timeseries_index_file_name = "db_timeseriesindex.dbdb"
		timeseriesIndexDB = DB.connect(timeseries_index_file_name)
		# Store number of time series stored
		timeseriesIndexDB.set("number_of_timeseries", "1000")
		# Store all the ids in one long list to minimize I/O - it's more efficient that way
		timeseriesIndexDB.set("timeseries_ids", ','.join(all1000IDs)) # Encode time series IDs into a comma-separated String
		timeseriesIndexDB.commit()

	# At this stage, we have all databases, we can work out the top k similar timeseries to return

	# Step 1: Find closest vantage point

	# First get all 20 vantage time series from the index DB
	vantageIndexDB = DB.connect(vantage_index_file_name) 
	vantageTS_all = []
	vantageID_all = []
	for i in range(num_vantage_points):
		vantageID = vantageIndexDB.get(str(i))
		vantageTS = fsm.get(vantageID)
		vantageTS_all.append(vantageTS)
		vantageID_all.append(vantageID)

	# Find the closest vantage ID from the 20
	vantageID_closest = ""
	minDistance = sys.maxsize
	for i in range(len(vantageTS_all)):
		vantageTS = vantageTS_all[i]
		vantageID = vantageID_all[i]
		distanceFromInputTS = kernel_dist(inputTS, vantageTS)
		if distanceFromInputTS < minDistance:
			minDistance = distanceFromInputTS
			vantageID_closest = vantageID

	# Step 2: Calculate 2r distance, and grab all the TimeSeries within 2r distance from RBT

	# Grab the time series IDs and distances that are within 2 * minDistance from closest vantage point
	radius = 2 * minDistance
	vantage_file_name = 'db_vantagepoint_' + vantageID_closest + ".dbdb"
	vantageDB = DB.connect(vantage_file_name)
	distance_ID_tuples = vantageDB._tree.chop(str(radius))

	# Convert distance id list of tuples to dictionary of ID to distance
	ID_distance_dict = {}
	for (distance, ID) in distance_ID_tuples:
		ID_distance_dict[ID] = distance

	# Sort dictionary of ID to distance based on ascending order of distance
	top_ID_distance_dict = sorted(ID_distance_dict, key=ID_distance_dict.get, reverse=False)[:num_top]
	top_TS = []

	# Return top ids:
	if int(id_or_ts) == 0:
		return top_ID_distance_dict
	
	for top_IDs in top_ID_distance_dict:
		top_TS.append(fsm.get(top_IDs))

	return(top_TS)

