import os
import logging
from app import app
from app.service import APIService
from flask import render_template, send_from_directory
from flask import Flask, request, abort, redirect, url_for, jsonify, make_response

import sys

sys.path.append(os.path.abspath("../")); from TSDBSerialize import Serialize
sys.path.append(os.path.abspath("../../MS2")); from FileStorageManager import FileStorageManager
sys.path.append(os.path.abspath("../../MS1")); from TimeSeries import TimeSeries

log = logging.getLogger(__name__)
service = APIService()

def _requiredLengthOfTimeSeries():
	'''
	Returns the constant - the required length of input time series
	'''
	return 4

@app.route('/')
def home():
	# TODO: This will eventually be replaced with Part 11 code for the index.html views
	timeseries = service.get_timeseries()
	return render_template('index.html', timeseries=timeseries)

@app.route('/timeseries', methods=['GET'])
def get_timeseries():
	'''
	Get time series metadata.
	Range queries define which time series are being fetched.
	'''
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
	'''
	Stores a new time series in the data stores (all 3)
	Might have to recalculate vantage points for every 50 new time series stored
	'''
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
	return jsonify(response), 201

@app.route('/timeseries/<string:tid>', methods=['GET'])
def get_timeseries_with_id(tid):
	'''
	Get time series metadata and the timeseries itself with provided id
	'''
	timeseries = service.get_timeseries_with_id(tid)
	return jsonify(timeseries), 200

@app.route('/simquery', methods=['GET'])
def get_simquery():
	'''
	Get top k similar time series with respect to the input id in the query string
	'''
	tid = request.args.get('id')
	# There must be the id of the id to perform simquery in the query
	if tid is None:
		abort(400, 'id param is not provided for simquery')
	k = request.args.get('k')
	if k is None or not isinstance(k, int):
		# If k not provided, default to finding top 5 similar timeseries
		k = 5

	# TODO: Send to socket server
	
	# Grab time series from FSM
	fsm = FileStorageManager()
	serialize = Serialize()
	timeseriesObject = fsm.get(key=tid)

	# Serialize and send to socket server
	timeseriesJSON = serialize.ts_to_json(timeseriesObject)
	timeseriesBytes = serialize.json_to_bytes(timeseriesJSON)

	log.info("Time series bytes in tid:")
	log.info(timeseriesBytes)
	
	# response = service.get_simquery(tid, k)
	# Return k closest time series from socket server
	return jsonify({'timeseries': []}), 200

@app.route('/simquery', methods=['POST'])
def post_simquery():
	'''
	Get top k similar time series with respect to the input time series in JSON form in 
	the POST body.
	'''
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

	# TODO: Serialize and send to socket server
	serialize = Serialize()
	timeseriesBytes = serialize.json_to_bytes(timeseries)

	log.info("Time Series Bytes:")
	log.info(timeseriesBytes)

	# When done with socket server to get the top k ids, get meta data and actual timeseries of timeseries found

	# response = service.post_simquery(timeseries, k)
	# Return k closest time series from socket server
	return jsonify({'timeseries': []}), 200

@app.route('/static/<string:directory>/<path:path>')
def send_static(directory, path):
	log.info('Static File Dir:%s, Path:%s', directory, path)
	return send_from_directory('static', os.path.join(directory, path))
