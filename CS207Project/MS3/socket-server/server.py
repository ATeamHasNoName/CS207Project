import sys
import logging
import json
import threading
import socket
import select
import binascii
import time
import numpy as np
from Distance_from_known_ts import Simsearch
from Distance_from_known_ts import FindTimeSeriesByKey
sys.path.append('../'); 
from TSDBSerialize import Serialize
sys.path.append('../MS1/');
from TimeSeries import TimeSeries
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface

log = logging.getLogger(__name__)

TIMEOUT = 30
SOCKETS = []
BUFFERSIZE = 65536  # TODO: Increase??
ARGUMENTS = 3
LINE = "============================================================================================"

def Server():
	
	if(len(sys.argv) < ARGUMENTS):
		print ('You typed in too few arguments.\n Please use the format: python server.py IP_ADDRESS PORT_NUMBER\n')
		e(2)
   
	num_of_client_requests = 0
 
	# Get port number from input:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	
	TEST = 0
	if sys.argv[3]:
		TEST = int(sys.argv[3])
	# Set up host socket:
	hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	# Bind host socket and listen to other sockets:
	hostSocket.bind((HOST, PORT))
	hostSocket.listen(True)
	
	# Add host server to SOCKETS:
	SOCKETS.append(hostSocket)
	
	print ("A brand new server has fired up using port: " + str(PORT) + "!\n")

	# First time server is started: Fill the database with dummy data:
	SS = Simsearch(load_ts_file("169975.dat_folded.txt"), 5, 1)

	wait_count = 0
	# Listen to potential incoming sockets:
	while True:
		empty = []

		# Used for testing purposes:
		if TEST > 0:
			wait_count += 1        
		if (TEST > 0 and wait_count == 100000):
		   e(0)

		# Fetch incoming sockets:
		incomingSockets,w,err = select.select(SOCKETS,empty,empty,0)

		for incomingSocket in incomingSockets:
			log.info("Incoming socket")
			# A new client has initiated a connection:
			if incomingSocket == hostSocket:
				d,_ = hostSocket.accept()
				SOCKETS.append(d)

			# Message from user received:
			else:
				try:
					# Increase number of client requests:
					num_of_client_requests += 1
					print("===================================== Client request #%i ==================================" % (num_of_client_requests))

					# Fetch data from the incoming socket:
					data = incomingSocket.recv(BUFFERSIZE)
					data = data.decode('utf-8')

					print("Server got an incoming request with data: %s\n" % (data))
					ts_or_id = data[0]
					length   = int(data[1:33]) # Length starts at character 1 and ends at 32
					k_closest   = int(data[33:65], 2) # Length starts at character 33 and ends at 64
					print(k_closest)
					ts_bytes    = data[65 : 65 + length]
					# Store key if id was sent from client:
					key = ts_bytes
					ts_bytes = bytes(ts_bytes, encoding='utf-8')
					
					# Fetch TS:
					if int(ts_or_id) == 1:
						# Convert bytes to json
						ts_json = Serialize().bytes_to_json(ts_bytes)
						# Convert json to TimeSeries:
						ts = Serialize().json_to_ts(ts_json)
						
						# Get top 5 ids and timeseries and convert to bytes:
						top_5_ids_and_ts_bytes = get_top_5_ids_and_ts_as_bytes(ts, k_closest)
					else:
						# Fetch from ID:
						ts_by_id = FindTimeSeriesByKey(key)
						# If ID is none then we let the client know and close the socket:
						if ts_by_id is None:
							id_not_in_database_string = "The id %s is not in the database.\n" % (key)
							SOCKETS[1].send(bytes(id_not_in_database_string, encoding='utf-8'))
							SOCKETS.remove(SOCKETS[1])
							print("Client sent invalid id to server. Connection to client closed.")
							print(LINE)
							continue

						# Get top 5 ids and timeseries and convert to bytes:
						top_5_ids_and_ts_bytes = get_top_5_ids_and_ts_as_bytes(ts_by_id, k_closest)

					print("Sent closest %i timeseries and ids to client" % (k_closest))
					print(LINE + "\n")

					# If we have a connection then send data to the socket:
					if SOCKETS[1]:
						SOCKETS[1].send(top_5_ids_and_ts_bytes)

					# Remove socket from SOCKET list: 
					SOCKETS.remove(SOCKETS[1])

				except:
					continue

def get_top_5_ids_and_ts_as_bytes(ts, k_closest):
	'''
	Takes in a TimeSeries and fetches the closest 5 ids and timeseries and returns it as bytes.

		Parameters
		----------
		ts: TimeSeries object

		Returns:
		--------
		Closest 5 TimeSeries and their Ids as json bytes
	'''
	# Get top 5 closest TimeSeries and ids:
	top_5_ids = Simsearch(ts, k_closest,0)
	top_5_ts = Simsearch(ts, k_closest,1)

	# Combine top 5 ids and ts to json:                        
	top_5_ids_and_ts = Serialize().ids_and_ts_to_json(top_5_ids, top_5_ts)

	# Convert them to bytes:
	top_5_ids_and_ts_bytes = bytes(str(top_5_ids_and_ts), encoding='utf-8')

	return top_5_ids_and_ts_bytes
 

def load_ts_file(filepath):
	'''
	Takes in file and reads time series from it

	Parameters
	----------
	filepath: path of the file 
	
	Returns
	-------
	timeSeries object : TimeSeries class

	>>> ts=load_ts_file('input.txt')
	>>> ts.values()[0]
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

def e(val):
	exit(val)

if __name__ == "__main__":
	sys.exit(Server())

