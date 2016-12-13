import logging
import numpy as np
import random
import sys
from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
from json import JSONEncoder

sys.path.append('../'); from TSDBSerialize import Serialize
sys.path.append('../../MS2/'); from FileStorageManager import FileStorageManager
sys.path.append('../../MS1/'); from TimeSeries import TimeSeries

log = logging.getLogger(__name__)


class ProductJSONEncoder(JSONEncoder):

	def default(self, obj):
		if isinstance(obj.__class__, DeclarativeMeta):
			return obj.to_dict()
		return super(ProductJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = ProductJSONEncoder

user = 'ubuntu'
password = 'cs207password'
host = 'localhost'
port = '5432'
db = 'ubuntu' 
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
app.config['SQLALCHEMY_DATABASE_URI'] = url # 'sqlite:////tmp/tasks.db'
db = SQLAlchemy(app)


class TimeSeriesModel(db.Model):
	'''
	Here is the corresponding PostgreSQL code:

	CREATE TYPE level AS ENUM ('A', 'B', 'C', 'D', 'E', 'F');
	CREATE TABLE timeseries (
		tid CHAR(32) PRIMARY KEY,
		mean float(16) NOT NULL,
		std float(16) NOT NULL,
		blarg float(16) NOT NULL,
		level level NOT NULL 
	);

	'''
	__tablename__ = 'timeseries'
	# Timeseries ID could be a string of up to length 32, not just restricted to Int
	tid = db.Column(db.String(32), primary_key=True) 
	mean = db.Column(db.Float, nullable=False)
	std = db.Column(db.Float, nullable=False)
	blarg = db.Column(db.Float, nullable=False)
	level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E', 'F', name='level'), nullable=False)

	def __repr__(self):
		return '<Timeseries %r>' % self.tid

	def to_dict(self):
		return dict(tid=self.tid, mean=self.mean, std=self.std, blarg=self.blarg, level=self.level)

"""
Timeseries code
"""

def _split_range(in_query):
	'''
	Takes in string of in_query, and returns the lower and upper limit of the range in a tuple
	Both lower and upper limit should be defined
	Returns None if in_query is malformed
	'''
	limits = in_query.split('-')
	if len(limits) != 2: # Query should have both a lower and upper limit
		return None, None
	try:
		lower = float(limits[0])
		upper = float(limits[1])
		return lower, upper
	except ValueError:
		return None, None

def _split_level(level_in_query):
	'''
	Takes in string of level_in_query, and returns the tuple form
	If empty no comma, treat the whole string as a level, which has similar behavior to "level equals" param
	'''
	levels = level_in_query.split(',')
	return tuple(levels)

@app.route('/timeseries', methods=['GET'])
def get_timeseries():
	# Extra credit: Support multiple queries at a time
	
	# Continuous variables only support in
	mean_in = request.args.get('mean_in')
	std_in = request.args.get('std_in')
	blarg_in = request.args.get('blarg_in')

	# Discrete variables support in and equals
	level_in = request.args.get('level_in')
	level = request.args.get('level')
	
	maxf = sys.maxsize
	minf = -sys.maxsize - 1    
	# Query for all ranges by default so we can support multiple queries
	mean_lower, mean_upper = minf, maxf
	std_lower, std_upper = minf, maxf
	blarg_lower, blarg_upper = minf, maxf

	if mean_in is not None:
		mean_lower, mean_upper = _split_range(mean_in)
		if mean_lower is None:
			abort(400)
	if std_in is not None:
		std_lower, std_upper = _split_range(std_in)
		if std_lower is None:
			abort(400)
	if blarg_in is not None:
		blarg_lower, blarg_upper = _split_range(blarg_in)
		if blarg_in is None:
			abort(400)

	# By default search for all levels
	levels = ('A', 'B', 'C', 'D', 'E', 'F')
	# If both provided, choose level as it is a stronger option
	if level is not None:
		levels = (level, level) # Need at least two elements to make it a tuple
	elif level_in is not None:
		levels = _split_level(level_in)

	timeseries_queried = TimeSeriesModel.query.filter(
		TimeSeriesModel.mean>mean_lower).filter(
		TimeSeriesModel.mean<mean_upper).filter(
		TimeSeriesModel.std>std_lower).filter(
		TimeSeriesModel.std<std_upper).filter(
		TimeSeriesModel.blarg>blarg_lower).filter(
		TimeSeriesModel.blarg<blarg_upper).filter(
		TimeSeriesModel.level.in_(levels)).all()

	log.info('Queried these timeseries metadata: ', timeseries_queried)

	return jsonify(dict(metadata=timeseries_queried)), 200

@app.route('/timeseries', methods=['POST'])
def create_timeseries():
	log.info("we're here in timeseries")
	# Request must be a JSON object that has the keys: tid and timeseries
	if (not request.json or not 'id' in request.json or not 'timeseries' in request.json):
		abort(400)
	tid = request.json['id']
	# Timeseries is dictionary/JSON of the format of {'key': value}
	timeseries = request.json['timeseries']
	if not isinstance(timeseries, dict):
		abort(400)
	
	# Get timeseries metadata and store it in PostgreSQL
	
	# Grab all the values of the timeseries
	values = list(timeseries.values())
	log.info(values)
	mean = np.mean(values)
	std = np.std(values, ddof=1)
	# To safeguard against timeseries with only one value which will return NaN std, we set std to 0 if it is NaN
	if np.isnan(std):
		std = 0.0

	# Draw blarg from a random uniform distribution of [0,1]
	blarg = np.random.uniform(0, 1)
	# Draw level from a random dice from 'A', 'B', 'C', 'D', 'E', 'F'
	levels = ['A', 'B', 'C', 'D', 'E', 'F']
	level = random.choice(levels)
	prod = TimeSeriesModel(tid=tid, mean=mean, std=std, blarg=blarg, level=level)
	db.session.add(prod)
	db.session.commit()

	# TODO: Update vantage points if necessary

	fsm = FileStorageManager()
	serialize = Serialize()
	# Convert the JSON object to a TimeSeries object to store it in FSM
	timeseriesObject = serialize.json_to_ts(timeseries)
	fsm.store(timeSeries=timeseriesObject, key=tid)
	
	return jsonify(timeseries), 201

@app.route('/timeseries/<string:tid>', methods=['GET'])
def get_timeseries_with_id(tid):
	# Return the timeseries metadata for this id
	timeseries = TimeSeriesModel.query.filter_by(tid=tid).first()

	if timeseries is None:
		log.info('Failed to get Timeseries with id=%s', tid)
		abort(404)
	log.info('Getting Timeseries with id=%s', tid)

	fsm = FileStorageManager()
	serialize = Serialize()
	timeseriesObject = fsm.get(key=tid)

	timeseriesJson = serialize.ts_to_json(timeseriesObject)
	
	return jsonify({'metadata': timeseries, 'timeseries': timeseriesJson}), 200

@app.route('/simquery', methods=['GET'])
def get_simquery():
	'''
	Get top k similar time series with respect to the input id in the query string
	'''
	tid = request.args.get('id')
	k = request.args.get('k')

	# TODO: Run part 7 vantage point code
	
	return jsonify({'timeseries': ''}), 200

@app.route('/simquery', methods=['POST'])
def post_simquery():
	'''
	Get top k similar time series with respect to the input time series in JSON form in 
	the POST body.
	'''
	timeseries = request.json['timeseries']
	k = request.json['k']

	# TODO: Run part 7 vantage point code 
	
	return jsonify({'timeseries': ''}), 200

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	db.create_all()
	app.run(port=5001)
