from random import normalvariate, random
from itertools import count
from StreamTimeSeriesInterface import StreamTimeSeriesInterface
class SimulatedTimeSeries(StreamTimeSeriesInterface):

	# (time, value)


	'''
	1) make_data, produce: You should be able to handle the case where the input is [value]: 
	your produce will take the k items and package them into (index, value). But if 
	there is time provided then you just output the (time, value). This means you have to 
	create two different make_data1, make_data2

	2) iter: iterate one by one by calling provided generator (do for all 4 iter functions)

	3) test_SimulatedTimeSeries.py: Look inside test_TimeSeries.py
	py.test --cov --cov-report term-missing SimulatedTimeSeries.py test_SimulatedTimeSeries.py

	4) write comments and doctests
	Doctests should not cover corner cases or invalid input, they should just include max of 1 or 2 tests that 
	explain how this function works 
	py.test --doctest-modules  --cov --cov-report term-missing SimulatedTimeSeries.py test_SimulatedTimeSeries.py
	'''



	#gen = produce()	# curr_index = 0
	#gen.next() # 0
	#gen.next() # 5
	#gen = produce() # 0

	'''
	def produce(k=5):
		curr_index = 0
		gen.:
			curr_index+=k
			yield 
	
	def __iter__(self):
		out=self.next()
		if isinstance(out,tuple):
				if len(out)>1:
					#print "time is provided"
					yield out[1]
		elif isinstance(out,tuple):
				if len(out)==1:
					yield out[0]
				else:
					yield out
	
		def produce(self,chunk=5):
			curr_index=0
			data_list=[]
			time=0
			
			for i in range(0,chunk):
				curr_index+=chunk
				out=self.next()
				if isinstance(out, (tuple)):
					if len(out)>1:
						#print "time is provided"
						data_list.append(out)
				else:
					data_list.append((time,out))
					time+=1

			return data_list
		
	def make_time_and_values(m,stop=None):
		for _ in count():
			if stop and _ > stop:
				break
			yield (_+0.1,1.0e09 + normalvariate(0, m*random()))


	def make_data(m, stop=None):
		time = range(0,1000)
	    for _ in count():
	        if stop and _ > stop:
	            break
	        yield 1.0e09 + normalvariate(0, m*random() ), time[i++]

	'''	
	def __init__(self,gen):
		#print("I'm constructing")
		self.gen=gen
		next(self.gen)
		#print("I've constructed")
		#print(next(self.gen))
		#print(self.produce())

	def kind_of_input(self,input):
		if isinstance(input, (tuple)):
			if len(input)==2:
				#print "time is provided"
				return "TimedTuple"
			elif len(input)==1:
				return "UnTimedTuple"
		else:
			return "float"

	def produce(self,chunk=1):
		data_list=[]
		firstout=next(self.gen)
		typeout=self.kind_of_input(firstout)
		if typeout=="TimedTuple":
			for i in range(0,chunk):
				data_list.append(next(self.gen))
			yield data_list
		if typeout=="UnTimedTuple":
			#print("UnTimedTuple")
			for i in range(0,chunk):
				tupledata=(i,next(self.gen)[0])
				data_list.append(tupledata)
			yield data_list
		if typeout=="float":
			#print("float")
			for i in range(0,chunk):
				tupledata=(i,next(self.gen))
				data_list.append(tupledata)
			yield data_list

	def __iter__(self):
		firstout=next(self.gen)
		typeout=self.kind_of_input(firstout)
		if typeout=="TimedTuple":
			yield firstout
		if typeout=="UnTimedTuple":
			yield (0,firstout[0])
		if typeout=="float":
			yield (0,firstout)

	def iteritems(self):
		yield next(self.gen)

	def itertimes(self):
		out=next(self.gen)
		if self.kind_of_input(out)=="TimedTuple":
			yield out[0]
		else:
			yield None

	def itervalues(self):
		out=next(self.gen)
		if self.kind_of_input(out)=="TimedTuple":
			yield out[1]
		elif self.kind_of_input(out)=="UnTimedTuple":
			yield out[0]
		else:
			yield out


