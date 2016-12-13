import os
import logging
import select
import socket
import signal
import json
from app import app
from collections import OrderedDict
from app.service import APIService
from flask import render_template, send_from_directory
from flask import Flask, request, abort, redirect, url_for, jsonify, make_response

import sys

sys.path.append(os.path.abspath("../")); from TSDBSerialize import Serialize
sys.path.append(os.path.abspath("../../MS2")); from DB import DB
sys.path.append(os.path.abspath("../../MS1")); from TimeSeries import TimeSeries

log = logging.getLogger(__name__)
service = APIService()

def _requiredLengthOfTimeSeries():
	'''
	Returns the constant - the required length of input time series
	'''
	return 4

@app.route('/428/<string:directory>/<path:path>')
def send_static(directory, path):
	"""
	Route static files via /428 as /static is a reserved keyword in nginx
	"""
	log.info('Static File Dir:%s, Path:%s', directory, path)
	return send_from_directory('static', os.path.join(directory, path))

@app.route('/')
def home():
	"""
	Single page with flot charts is presented at /
	"""
	# TODO: To remove this
	# timeseries = service.get_timeseries()
	# Return all indexes back to index.html to display in drop down list
	timeseries_index_file_name = "db_timeseriesindex.dbdb"
	timeseriesIndexDB = DB.connect(timeseries_index_file_name)
	timeseries_ids = timeseriesIndexDB.get("timeseries_ids")
	# Convert comma-separated ids into arrays
	return render_template('index.html', timeseries=timeseries_ids.split(','))

@app.route('/timeseries', methods=['GET'])
def get_timeseries():
	"""
	Get time series metadata.
	Range queries define which time series are being fetched.
	"""
	# Grab all params if there are present
	mean_in = request.args.get('mean_in')
	std_in = request.args.get('std_in')
	blarg_in = request.args.get('blarg_in')
	level_in = request.args.get('level_in')
	level = request.args.get('level')
	timeseries = service.get_timeseries(mean_in=mean_in, std_in=std_in, blarg_in=blarg_in, level_in=level_in, level=level)
	return jsonify(timeseries), 200

@app.route('/timeseries', methods=['POST'])
def create_timeseries():
	"""
	Stores a new time series in the data stores (all 3)
	Might have to recalculate vantage points for every 50 new time series stored
	"""
	# Request must be a JSON object that has the keys: tid and timeseries
	if (not request.json or not 'id' in request.json or not 'timeseries' in request.json):
		abort(400, 'Input time series is not a json object, does not have an id key or does not have a timeseries key')
	tid = request.json['id']
	# Timeseries is dictionary/JSON of the format of {'key': value}
	timeseries = request.json['timeseries']
	if not isinstance(timeseries, dict) or len(timeseries) != _requiredLengthOfTimeSeries():
		abort(400, ('Input time series is not a json object or its length of %s is not %s') % (str(len(timeseries)), str(_requiredLengthOfTimeSeries())))
	# Timeseries must be correct length
	response = service.create_timeseries(tid, timeseries)
	# TODO: Send tid and timeseries to socket server to store it there

	return jsonify(response), 201

@app.route('/timeseries/<string:tid>', methods=['GET'])
def get_timeseries_with_id(tid):
	"""
	Get time series metadata and the timeseries itself with provided id
	"""
	metadata = service.get_timeseries_with_id(tid)
	# TODO: Now get actual timeseries object from Socket Server

	return jsonify(metadata), 200

def _binaryLength32(length):
	"""
	Private helper function for connecting to socket server that returns the binary length of string.

	Parameters
	----------
	length: the length of the string 
	
	Returns
	-------
	the length of the string in 32 bit binary

	>>> st = "CS207"
	>>> st_length = len(st)
	>>> st_binary_length = binaryLength32(st_length)
	>>> st_binary_length
	'00000000000000000000000000000101'
	"""
	return format(length, '032b')

def _getClosestTimeSeries_from_socket_server(k_closest, ts_or_id, timeseriesID=None, timeseriesJSON=None):
	"""
	Function to connect to the socket server and pass over the timeseries ID or time series JSON 
	in order to get the closest time series.
	"""
	host = "localhost"
	port = 5002
	BUFFERSIZE = 65536

	# Converts either ID or JSON
	ts_json = 0
	if int(ts_or_id) == 1: # 1 stands for JSON
		ts_json = Serialize().json_to_jsonstring(timeseriesJSON)
	else: # 0 stands for ID
		ts_json = timeseriesID

	# Set up socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	s.settimeout(3)

	# Try to connect to the server
	try :
		log.info("Connecting to IP: %s" % (host))
		log.info("Connecting to port: %s\n" % (port))
		s.connect((host, port))
	except :
		log.info('Cannot connect to the server. IP address provided or port number might be wrong or host is not up.\n')
		raise ValueError('Issue with socket server')

	ts_to_json_LengthBinary = _binaryLength32(len(ts_json))
	k_closest_LengthBinary = _binaryLength32(k_closest)

    # Format sent to server is:
    # 0/1: id is 0, ts is 1        [Starts at byte number 1]
    # length of id / ts in 32 bits [Starts at byte number 2]
    # k_closest                    [Starts at byte number 34]
    # value of id or ts            [Starts at byte number 66]
	sendTsOrIdToServer = str(ts_or_id) + ts_to_json_LengthBinary + k_closest_LengthBinary + ts_json

	if (int(ts_or_id) == 0):
		print("Sending id to server")
	else:
		print("Sending TimeSeries to server")

	s.send(Serialize().jsonstring_to_bytes(sendTsOrIdToServer))
	print("Data is encoded as: %s\n" % (bytes(sendTsOrIdToServer, encoding='utf-8')))

	while True:
		empty = []
		# Fetch sockets from server
		availableSockets = [sys.stdin, s]
		sockets, write, error = select.select(availableSockets, empty, empty)

		for incomingSocket in sockets:
			if incomingSocket == s:
				log.info("Got a response from server.\n")
				closestTimeseriesBuffer = incomingSocket.recv(BUFFERSIZE)
				closestTimeseriesBuffer = closestTimeseriesBuffer.decode()
				# Converts buffer to JSON string
				closestTimeseriesString = str(closestTimeseriesBuffer).replace("'", '"')
				s.shutdown(socket.SHUT_RDWR)
				s.close()
				log.info(closestTimeseriesString)

				# Convert JSON string to JSON object and return
				return json.loads(closestTimeseriesString)

@app.route('/simquery', methods=['GET'])
def get_simquery():
	"""
	Get top k similar time series with respect to the input id in the query string
	"""
	tid = request.args.get('id')
	# There must be the id of the id to perform simquery in the query
	if tid is None:
		abort(400, 'id param is not provided for simquery')
	k = request.args.get('k')
	if k is None or not isinstance(k, int):
		# If k not provided, default to finding top 5 similar timeseries
		k = 5
	
	# TODO: Send to socket server
	closestTimeseries = _getClosestTimeSeries_from_socket_server(k_closest=k, ts_or_id=0, timeseriesID=tid)

	# Get back nearest k TimeSeries json in {"id1": {"key1": v1, ...}, ...} format
	
	# Get the metadata of the closest timeseries from the API
	tid_in = ','.join(map(str, closestTimeseries.keys()))
	metadata = service.get_timeseries(tid_in=tid_in)

	# Sort closestTimeseries by keys
	closestTimeseries = OrderedDict(sorted(closestTimeseries.items()))

	log.info("metadata in simquery:")
	log.info(metadata)
	log.info(metadata["metadata"])

	return jsonify({'timeseries': closestTimeseries, 'metadata': metadata["metadata"]}), 200

@app.route('/simquery', methods=['POST'])
def post_simquery():
	"""
	Get top k similar time series with respect to the input time series in JSON form in 
	the POST body.
	"""
	if (not request.json or not 'timeseries' in request.json):
		abort(400)
	# Timeseries is dictionary/JSON of the format of {'key': value}
	timeseries = request.json['timeseries']
	if not isinstance(timeseries, dict) or len(timeseries) != _requiredLengthOfTimeSeries():
		abort(400, ('Input time series is not a json object or its length of %s is not %s') % (str(len(timeseries)), str(_requiredLengthOfTimeSeries())))
	k = request.json['k']
	if k is None or not isinstance(k, int):
		# If k not provided, default to finding top 5 similar timeseries
		k = 5

	# TODO: test this with actual client code
	closestTimeseries = _getClosestTimeSeries_from_socket_server(k_closest=k, ts_or_id=1, timeseriesJSON=timeseries)

	# Get the metadata of the closest timeseries from the API
	tid_in = ','.join(map(str, closestTimeseries.keys()))
	metadata = service.get_timeseries(tid_in=tid_in)

	# Sort closestTimeseries by keys
	closestTimeseries = OrderedDict(sorted(closestTimeseries.items()))

	log.info("metadata in simquery:")
	log.info(metadata)
	log.info(metadata["metadata"])
	return jsonify({'timeseries': closestTimeseries, 'metadata': metadata["metadata"]}), 200

