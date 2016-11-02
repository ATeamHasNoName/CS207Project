from random import normalvariate, random
from itertools import count
from StreamTimeSeriesInterface import StreamTimeSeriesInterface
class SimulatedTimeSeries(StreamTimeSeriesInterface):
	'''
	WORKFLOW - 
	RELEVANT FILES: 1) This class inherits from the StreamTimeSeriesInterface which is written in the file 
					StreamTimeSeriesInterface.py
					2) The test file for this class is test_SimulatedTimeSeries.py 
						The tests for this file can be run by using this command in the project directory -
						py.test --cov --cov-report term-missing SimulatedTimeSeries.py test_SimulatedTimeSeries.py

	A BRIEF DESCRIPTION OF THE METHODS in this class:
	1)Produce(): It is like an __iter__ function which can move multiple elements at a time. 
			It should be able to handle the case where the input is
				a) Tuple like (time,value)
				b) Tuple like (time,)
				c) Just a float value without time

			Produce will take the chunk=k and generator that was passed to the SimulatedTimeSeries object 
			and then call next on generator k times, so it is like a generator of generators.
			
			Most importantly, independent of the input type it will package it into (time, value). If 
			there is time provided it uses the provided time, otherwise generates an index everytime it is called.
			Since there is no underlying storage for this type of data, there is no "memory" of time. everytime
			new data is produced it is like a new list to be processed.

	2)__iter__(): Iterates over the provided generator one value at a time. But, since this is the default function
			that will be called when iterating over the generator, it has to account for the three kinds of data 
			input explained above. So, it must always package the data into a (time,value) tuple, independent
			of the kind of input.

	3) kind_of_input() : is a helper function created to handle the different kinds of input as explained above. 
			It can account for three kinds of input (mentioned above). These are named "TimedTuple", "UnTimedTuple"
			and "float" for convenience.

	4) __init__() : The constructor takes as input a generator function (which is assumed to generate) data that is
			of one of the three types defined above.

	5) iteritems(): The way iteritems is defined here is that it is different from __iter__. While __iter__ doesn't
			care about the original structure of the data passed, and always packages into a (time,value) data, 
			iteritems preserves the structure of the original generator passed, and just advances the generator
			by one everytime it is called.

	6) itervalues(): This function takes the generator and iterates over the values of the generator passed. As all generators
			assume that values are provided, it gives a valid output for all three kinds of data
	
	7) itertimes() : This function takes the generator and iterates over the time, instead of values. Since the time is originally
			provided only for one of the three kinds of inputs, it returns a valid output only for a TimedTuple,
			and returns a None for the other two kinds of input if called. 

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


