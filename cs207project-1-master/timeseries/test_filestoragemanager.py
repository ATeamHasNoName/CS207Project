from pytest import raises
from filestoragemanager import FileStorageManager
from arraytimeseries import ArrayTimeSeries
import numpy as np
import os

def test_filestoragemanager():

	fsm = FileStorageManager()
	ts = ArrayTimeSeries(times=[2,6,11,17,25], values=[10,12,22,34,40])

	# verify the time series
	assert ts[2] == 22

	unique_id = fsm.get_unique_id()
	fsm.store(unique_id, ts)
	stored_ts = fsm.get(unique_id)

	# verify that the retrieved time series matches and values are 64-bit floats
	assert stored_ts[2] == 22.0
	assert isinstance(stored_ts[2], np.float64) == True

	# verify that a new .json map file can be created
	# remove the file if it is present
	os.remove('id_length_map.json')

	# have the file storage manager create a new one and store a time series
	fsm = FileStorageManager()
	fsm.store(unique_id, ts)

	remove_test_files()

def test_filestoremanager_int_as_id():
	fsm = FileStorageManager()
	ts = ArrayTimeSeries(times=[2,6,11,17,25], values=[10,12,22,34,40])

	# try an int instead of using get_unique_id
	int_id = 2
	fsm.store(int_id, ts)

	remove_test_files()

def test_size():
	fsm = FileStorageManager()
	ts = ArrayTimeSeries(times=[2,6,11,17,25], values=[10,12,22,34,40])
	unique_id = fsm.get_unique_id()
	fsm.store(unique_id, ts)
	stored_ts = fsm.get(unique_id)

	# incorrect value should return -1
	assert fsm.size(99999999) == -1

	# correct value should return the size
	assert fsm.size(unique_id) == 5

	remove_test_files()

def test_get_return_none():
	fsm = FileStorageManager()
	ts = ArrayTimeSeries(times=[2,6,11,17,25], values=[10,12,22,34,40])
	unique_id = fsm.get_unique_id()
	fsm.store(unique_id, ts)

	# invalid id should return None
	assert fsm.get(9999999999) == None

	remove_test_files()

def remove_test_files():
	test_files = ['1.npy','2.npy', 'ts_1.npy', 'ts_2.npy', 'ts_3.npy', 'ts_4.npy', 'id_length_map.json']
	for i in test_files:
		if os.path.exists(i):
			os.remove(i)