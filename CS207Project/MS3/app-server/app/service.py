import requests
import logging

log = logging.getLogger(__name__)

class APIService(object):

	def __init__(self, url='localhost', port=5001):
		self.url = url
		self.port = port

	def get_timeseries(self, mean_in=None, std_in=None, blarg_in=None, level_in=None, level=None, tid_in=None):
		endpoint = 'http://{}:{}/timeseries'.format(self.url, self.port)
		response = requests.get(endpoint, params={'mean_in': mean_in, 'std_in': std_in, 'blarg_in': blarg_in, 'level_in': level_in, 'level': level, 'tid_in': tid_in})
		if response.status_code in [400]:
			raise ValueError('timeseries could not be retrieved, perhaps you specified an incorrect range query')
		json_response = response.json()
		if json_response:
			log.debug('Response body %s', json_response)
			return json_response
		raise ValueError('no timeseries found')

	def create_timeseries(self, tid, timeseries):
		endpoint = 'http://{}:{}/timeseries'.format(self.url, self.port)
		response = requests.post(endpoint, json={'id': tid, 'timeseries': timeseries})
		if response.status_code in [200, 201]:
			json_response = response.json()
			return json_response
		raise ValueError('timeseries already exists')

	def get_timeseries_with_id(self, tid):
		endpoint = 'http://{}:{}/timeseries/{}'.format(self.url, self.port, tid)
		response = requests.get(endpoint)
		json_response = response.json()
		if json_response:
			log.debug('Response body %s', json_response)
			return json_response
		raise ValueError('no timeseries found')

	# def get_simquery(self, tid, k):
	# 	endpoint = 'http://{}:{}/simquery'.format(self.url, self.port)
	# 	# Pass in k and timeseries id in the params
	# 	response = requests.get(endpoint, params={'k': k, 'id': tid})
	# 	# If input tid is not in data store, return error
	# 	if response.status_code in [400]:
	# 		raise ValueError('Input tid is not in data store')
	# 	json_response = response.json()
	# 	if json_response:
	# 		log.debug('Response body %s', json_response)
	# 		return json_response
	# 	raise ValueError('no timeseries found')

	# def post_simquery(self, timeseries, k):
	# 	endpoint = 'http://{}:{}/simquery'.format(self.url, self.port)
	# 	# Pass in k and timeseries json object in the body
	# 	response = requests.post(endpoint, json={'k': k, 'timeseries': timeseries})
	# 	json_response = response.json()
	# 	if json_response:
	# 		log.debug('Response body %s', json_response)
	# 		return json_response
	# 	raise ValueError('no timeseries found')

