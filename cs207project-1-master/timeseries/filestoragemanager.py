from storagemanagerinterface import StorageManagerInterface
from arraytimeseries import ArrayTimeSeries
import numpy as np
import json

class FileStorageManager(StorageManagerInterface):
	"""
		This class inherits from the StorageManagerInterface ABC and implements it by putting 2-d numpy
		arrays with 64-bit floats for both times and values onto disk. 

		NOTES
		-----
		PRE: It supports access to the time series in memory both on get and store calls by managing 
		a class variable self._id_dict

		Examples:
		---------
		>>> fsm = FileStorageManager()
		>>> ts = ArrayTimeSeries(times=[2,6,11,17,25], values=[10,12,22,34,40])
		>>> unique_id = fsm.get_unique_id()
		>>> fsm.store(unique_id, ts)
		array(...
		>>> stored_ts = fsm.get(unique_id)
		>>> assert stored_ts[2] == 22.0
	"""
	def __init__(self):
		"""
		 The manager maintains a persistent structure in memory and on disk which maps ids to the 
		 appropriate files and keeps track of lengths. It creates an on disk json file to store 
		 an id/length map or, if one already exists, updates the map.
		"""

		# set the file name for the time series id/length map
		file_path = 'id_length_map.json'

		# if the map file already exists, open it
		try:
			id_length_map = open(file_path, 'r')
			self._id_dict = json.load(id_length_map)
		except IOError:
			# if the file does not exist, create a new dict to be saved to disk in the store() method
			self._id_dict = dict()

	def get_unique_id(self):
		"""
		Description
		-----------
		Method used to create a new and unique id.

		Parameters
		----------
		self: Instance of subclass of StorageManagerInterface.

		Returns
		-------
		int : the newly created unique id
		"""

		# start the ids at 1
		i = 1

		# loop through the id/length map to determine the next unique id
		while True:

			# this string represents the name of the file stored on disk for this time series
			new_id = 'ts_datafile_' + str(i)

			# this is a unique id, return it
			if new_id not in self._id_dict:
				return new_id

			# the id was not unique, increment and continue the loop
			i += 1

	def store(self, id, t):
		"""
		Description
		-----------
		Method used to store a time series using the storage manager. 

		Parameters
		----------
		self: Instance of subclass of StorageManagerInterface.

		id : int
			Used as an identification of a particular time series being stored.

		t : SizedContainerTimeSeriesInterface
			A time series associated with SizedContainerTimeSeriesInterface
			that allows for time series data persistence.

		Returns
		-------
		SizedContainerTimeSeriesInterface
		"""

		# verify that the provided id is an int and convert it to a string
		if isinstance(id, int):
			id = str(id)

		# convert the time series to 2-d numpy array with 64-bit floats for both times and values
		ts = np.vstack((t.times(), t.values())).astype(np.float64)

		# save the time series to disk as a binary file in .npy format
		np.save(str(id), ts)

		# update the id/length map in memory for this store
		self._id_dict[id] = len(t.times())

		# update the id/length map on disk for this store
		# store the map as a json file
		with open("id_length_map.json", "w") as outfile:
			json.dump(self._id_dict, outfile)

		# return this instance of SizedContainerTimeSeriesInterface
		return ts

	def size(self, id):
		"""
		Description
		-----------
		Method used to return the size of a particular time series stored based on the 
		provided id.

		Parameters
		----------
		self: Instance of subclass of StorageManagerInterface.

		id : int
			The id of the time series of interest.

		Returns
		-------
		int : the size of the time series in question.

		Notes
		-----
		POST: returns -1 if no time series is found using the provided id
		"""

		# the id should be a string
		if not isinstance(id, str):
			id = str(id)

		# if there is a time series file for the provided id, return the size
		if id in self._id_dict:
			return self._id_dict[id]

		# no time series file was found, return -1
		else:
			return -1

	def get(self, id):
		"""
		Description
		-----------
		Method used to return a particular time series stored based on the 
		provided id.

		Parameters
		----------
		self: Instance of subclass of StorageManagerInterface.

		id : int
			The id of the time series of interest.

		Returns
		-------
		SizedContainerTimeSeriesInterface : the time series data requested by id.
		"""

		# it should be a string
		if not isinstance(id, str):
			id = str(id)

		# if the id is present in the map
		if id in self._id_dict:

			# load the numpy data from the binary file associated with the provided id
			ts = np.load(id + ".npy")

			# return a SizedContainerTimeSeriesInterface instance
			return ArrayTimeSeries(ts[0], ts[1])
		else:
			return None

"""
	Create a single instance of the FileStorageManager class. This is used in
	SMTimeSeries for delegation in methods that are implemented to satisfy interface
	requirements for SizedContainerTimeSeriesInterface.
"""
FileStorageManagerSingleton = FileStorageManager()