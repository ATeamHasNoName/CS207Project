import os
import logging
from app import app
from app.service import APIService
from flask import render_template, send_from_directory
from flask import Flask, request, abort, redirect, url_for, jsonify, make_response

log = logging.getLogger(__name__)
service = APIService()

@app.route('/')
def home():
	# TODO: This will eventually be replaced with Part 11 code for the index.html views
	timeseries = service.get_timeseries()
	return render_template('index.html', timeseries=timeseries)

@app.route('/timeseries', methods=['GET'])
def get_timeseries():
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
	# Request must be a JSON object that has the keys: tid and timeseries
	if (not request.json or not 'id' in request.json or not 'timeseries' in request.json):
		abort(400)
	tid = request.json['id']
	# Timeseries is dictionary/JSON of the format of {'key': value}
	timeseries = request.json['timeseries']
	if not isinstance(timeseries, dict):
		abort(400)
	response = service.create_timeseries(tid, timeseries)
	return jsonify(response), 201

@app.route('/timeseries/<string:tid>', methods=['GET'])
def get_timeseries_with_id(tid):
	timeseries = service.get_timeseries_with_id(tid)
	return jsonify(timeseries), 200

@app.route('/static/<string:directory>/<path:path>')
def send_static(directory, path):
	log.info('Static File Dir:%s, Path:%s', directory, path)
	return send_from_directory('static', os.path.join(directory, path))
