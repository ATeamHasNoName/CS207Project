import logging
import numpy as np
import random
import sys
from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
from json import JSONEncoder

# Duplicate corr here to allow regeneration of vantage points (Extra Credit)
from _corr import *
sys.path.append('../'); from TSDBSerialize import Serialize
sys.path.append('../../MS2/'); 
from FileStorageManager import FileStorageManager
from DB import DB
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
num_vantage_points = 5


class TimeSeriesModel(db.Model):
	'''
	Here is the corresponding PostgreSQL code:

	CREATE TYPE level AS ENUM ('A', 'B', 'C', 'D', 'E', 'F');
	CREATE TABLE timeseries (
		tid VARCHAR(32) PRIMARY KEY,
		mean float(16) NOT NULL,
		std float(16) NOT NULL,
		blarg float(16) NOT NULL,
		level level NOT NULL 
	);

	'''
	__tablename__ = 'timeseries'
	# Timeseries ID could be a string of up to length 32, not just restricted to Int
	tid = db.Column(db.String, primary_key=True) 
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

def _split_commas(comma_separated_query):
	'''
	Takes in string of level_in_query, and returns the tuple form
	If empty no comma, treat the whole string as a level, which has similar behavior to "level equals" param
	'''
	elements = comma_separated_query.split(',')
	return tuple(elements)

@app.route('/timeseries', methods=['GET'])
def get_timeseries():

	# Extra: Allows query by timeseries ids, tid_in=<id1>,<id2> in a similar format to level_in
	tid_in = request.args.get('tid_in')
	if tid_in is not None:
		# Specific query for tids, do not mix with the other range queries
		tids = _split_commas(tid_in)
		timeseries_queried = TimeSeriesModel.query.filter(
			TimeSeriesModel.tid.in_(tids)).order_by(TimeSeriesModel.tid).all()
		return jsonify(dict(metadata=timeseries_queried)), 200

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
		levels = _split_commas(level_in)

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

@app.route('/generatemetadata', methods=['POST'])
def generate_metadata():
	"""
	Being used by socket server to generate meta data for the 1000 time series
	"""
	# Request must be a JSON object that has the keys: tid and timeseries
	if (not request.json or not 'id' in request.json or not 'timeseries' in request.json):
		abort(400)
	tid = request.json['id']
	# Timeseries is dictionary/JSON of the format of {'key': value}
	timeseries = request.json['timeseries']
	if not isinstance(timeseries, dict):
		abort(400)
	_generate_metadata(tid=tid, timeseries=timeseries)
	return jsonify({"tid": tid}), 201

def _generate_metadata(tid, timeseries):
	"""
	Private helper function to generate metadata with input tid and timeseries JSON
	"""
	# Get timeseries metadata and store it in PostgreSQL
	
	# Grab all the values of the timeseries
	values = list(timeseries.values())
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

def _storeTimeSeriesInFSM(timeSeriesObject, key):
	"""
	Stores the time series object in FSM. This is being called by /timeseries POST on creation of a new time series.
	"""
	fsm = FileStorageManager()
	genKey = fsm.store(timeSeries=timeSeriesObject, key=key)
	
	# Update time series index
	timeseries_index_file_name = "db_timeseriesindex.dbdb"
	timeseriesIndexDB = DB.connect(timeseries_index_file_name)		
	
	num_timeseries = int(timeseriesIndexDB.get("number_of_timeseries"))
	timeseriesIndexDB.set("number_of_timeseries", str(num_timeseries + 1))

	timeseries_ids = timeseriesIndexDB.get("timeseries_ids")
	timeseriesIndexDB.set("timeseries_ids", timeseries_ids + "," + genKey)
	timeseriesIndexDB.commit()
	
	# Also update vantage points
	vantage_index_file_name = "db_vantageindex.dbdb"
	vantageIndexDB = DB.connect(vantage_index_file_name)

	# Calculate kernel dist from this new time series to each vantage, and update all 20 RBTs
	for i in range(num_vantage_points): # 20 vantage points
		vantageID = vantageIndexDB.get(str(i))
		vantageTS = fsm.get(vantageID)
		distanceFromInputTS = kernel_dist(timeSeriesObject, vantageTS)
		# Store this distance and the time series key inside the respective RBT
		vantage_file_name = 'db_vantagepoint_'+ vantageID + '.dbdb'
		vantageDB = DB.connect(vantage_file_name)
		vantageDB.set(str(distanceFromInputTS), genKey)
		vantageDB.commit()

	# Check if there are more than 50 new time series being added. If so, regenerate vantage points.
	if num_timeseries + 1 % 50 == 0:
		_regenerateVantagePoints()

def _regenerateVantagePoints():
	"""
	Vantage points are regenerated for every 50 time series added
	"""
	# Taking all points in timeseries index, sample 20 new ones as vantage points, and rebuild red black trees
	
	timeseries_index_file_name = "db_timeseriesindex.dbdb"
	timeseriesIndexDB = DB.connect(timeseries_index_file_name)		

	num_timeseries = int(timeseriesIndexDB.get("number_of_timeseries"))

	# Sample new vantage point indexes
	vantage_point_indexes = random.sample(range(num_timeseries), num_vantage_points)

	# Get actual vantage point ids
	timeseries_ids = timeseriesIndexDB.get("timeseries_ids").split(',')

	vantageIndexDB = DB.connect(vantage_index_file_name)
	vantageLabel = 0
	for i in vantage_point_indexes:
		vantageID = all1000IDs[i]
		vantageIndexDB.set(str(vantageLabel), vantageID)
		vantageLabel += 1
	vantageIndexDB.commit()


	return ""

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
	
	_generate_metadata(tid=tid, timeseries=timeseries)

	# Also store time series inside FSM
	_storeTimeSeriesInFSM(timeSeriesObject=Serialize().json_to_ts(timeseries), key=tid)
	# FileStorageManager().store(timeSeries=Serialize().json_to_ts(timeseries), key=tid)

	# TODO: Update the time series index: db_timeseriesindex.dbdb
	

	# Regenerate vantage points if necessary
	
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

# @app.route('/simquery', methods=['GET'])
# def get_simquery():
# 	'''
# 	Get top k similar time series with respect to the input id in the query string
# 	'''
# 	tid = request.args.get('id')
# 	k = request.args.get('k')

# 	# TODO: Run part 7 vantage point code
	
# 	return jsonify({'timeseries': ''}), 200

# @app.route('/simquery', methods=['POST'])
# def post_simquery():
# 	'''
# 	Get top k similar time series with respect to the input time series in JSON form in 
# 	the POST body.
# 	'''
# 	timeseries = request.json['timeseries']
# 	k = request.json['k']

# 	# TODO: Run part 7 vantage point code 
	
# 	return jsonify({'timeseries': ''}), 200

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	db.create_all()
	app.run(port=5001)
