from flask import Flask, jsonify, make_response, abort, request

app = Flask(__name__)

@app.route('/')
def index():
	# Define Web UI?
	return "Welcome to ATeamHasNoName"

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Endpoint not found. Try: /timeseries'}), 404)

@app.route('/timeseries', methods=['GET'])
def get_timeseries_metadata():
	# First check if there are queries
	# Extra credit? Support multiple queries at a time
	
	# Continuous variables only support in
	mean_in = request.args.get('mean_in')
	std_in = request.args.get('std_in')
	blarg_in = request.args.get('blarg_in')

	# Discrete variables support in and equals
	level_in = request.args.get('level_in')
	level = request.args.get('level')
	# If both provided, choose level as it is a stronger option

	# Write SQL statements to get from DB
	
	# Send json of all meta data if no range
	return 'Return all timeseries\n', 200

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
	# TODO: Store it in DBs
	return jsonify(timeseries), 201

@app.route('/timeseries/<int:tid>', methods=['GET'])
def get_timeseries_by_key(tid):
	# Send back metadata and time series data in a JSON
	return 'Return timeseries %d\n' % tid, 200

@app.route('/simquery', methods=['GET'])
def get_topk_similar_ids():
	'''
	Get top k similar time series with respect to the input id in the query string
	'''
	tid = request.args.get('id')
	topk = request.args.get('k')
	if topk is None or not isinstance(topk, int):
		# If k not provided, default to finding top 5 similar timeseries to tid
		topk = 5

	return 'Return timeseries %d\n' % tid, 200

@app.route('/simquery', methods=['POST'])
def get_topk_similar_ids_from_json():
	'''
	Get top k similar time series with respect to the input time series in JSON form in 
	the POST body.
	'''
	if (not request.json or not 'timeseries' in request.json):
		abort(400)
	# Timeseries is dictionary/JSON of the format of {'key': value}
	timeseries = request.json['timeseries']
	if not isinstance(timeseries, dict):
		abort(400)
	topk = request.json['k']
	if topk is None or not isinstance(topk, int):
		# If k not provided, default to finding top 5 similar timeseries to tid
		topk = 5
	return 'Return top %d time series\n' % topk, 200

if __name__ == '__main__':
	app.run(debug=False)
