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
		"""
		Initializes a SimulatedTimeSeries instance with the generator passed to it. It intitates the generator,
		sets it equal to self.gen, thereby making it available to all other methods in the class. 

		Further, it primes the generator by calling a next on it!

		Parameters
		----------
		gen : As explained above as well, this class is designed to handle three different kinds of generator
			  inputs - 
			  a) Tuple like (time,value)
			  b) Tuple like (time,)
			  c) Just a float value without time 

		Returns
		-------
		SimulatedTimeSeries
			A Simulated time series object with generator as the parameter. 
		
		>>> def generator_with_time(stop=None):
				_=0
				while 1:
					yield (_+0.1,_+0.5)
					_+=1
		>>> Obj_with_time=SimulatedTimeSeries(generator_with_time())
		>>> print(Obj_with_time)
		<SimulatedTimeSeries.SimulatedTimeSeries object at 0x101c8f518>
		"""
		
		self.gen=gen
		next(self.gen)

	def kind_of_input(self,input):
		'''
		This is a helper function defined to handle the fact that different kinds of inputs can be given.

		Parameters
		----------
		input : Can be of three kinds - 
				a) a tuple of length 2
				b) a tuple of length 1
				c) a float value 
		
		Returns
		-------
		A string which can take three values, depending upon the kind of input.

		If the provided input is a tuple of length 2, it returns "TimedTuple", i.e. it tells the subsequent
		functions that the input data is of the form (time,value)

		If the provided input is a tuple of length 1, it returns "UnTimedTuple", i.e. it tells the subsequent
		functions that the input data is of the form (value,)

		If the provided input is a float, it returns "float", i.e. it tells the subsequent
		functions that the input data is of the form float values.


		>>> k=2.3
		>>> obj.kind_of_input(2.3)
		"float"
		>>> obj.kind_of_input((4,3))
		"TimedTuple"		
		>>> obj.kind_of_input((7,))
		"UnTimedTuple"
		'''
		if isinstance(input, (tuple)):
			if len(input)==2:
				#print "time is provided"
				return "TimedTuple"
			elif len(input)==1:
				return "UnTimedTuple"
		else:
			return "float"

	def produce(self,chunk=1):
		"""
		Moves the generator function by a size = the chunk variable. 

		Accounts for the three different kinds of inputs that can be provided to it, and then packages
		the result into a (time,value) tuple.

		NOTE : Since this is a storage-less implementation as mentioned in the HW guidelines, it is important
		to note that there is no pre existing index of values for time, or in other words, there is no memory
		of things generated the last time the function was called. Thus, everytime a new chunk is generated, 
		if there is no time already provided, the counter for the index (which also serves as the time if not provided)
		restarts from scratch! It also makes sense given the applications mentioned in examples in guidelines.

		Parameters
		----------
		chunk : Defines the number of moves the generator should be moved by. Produce can be thought of 
		as a generator of generators, as it takes a generator and moves it by "chunk" units.

		Returns
		-------
		A genertor object. 

		In order to proceed it, we need to do a next() on it!
		>>> def generator_with_time(stop=None):
				_=0
				while 1:
					yield (_+0.1,_+0.5)
					_+=1
		>>> Obj_with_time=SimulatedTimeSeries(generator_with_time())
		>>> print(next(Obj_with_time.produce(chunk=2)))
		((0.1,0.5),(1.1,1.5))
		"""
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
		'''
		Does the exact same thing as above, but just moves by one! So, returns a generator as well.
		Parameters
		----------
		None

		Returns
		-------
		In order to proceed it, we need to do a next() on it!
		>>> def generator_with_time(stop=None):
				_=0
				while 1:
					yield (_+0.1,_+0.5)
					_+=1
		>>> obj1=SimulatedTimeSeries(generator_with_time())
		>>> def test_iter_with_time():
				for a in obj1:
					print a 
		(0.1, 0.5)
		'''
		firstout=next(self.gen)
		typeout=self.kind_of_input(firstout)
		if typeout=="TimedTuple":
			yield firstout
		if typeout=="UnTimedTuple":
			yield (0,firstout[0])
		if typeout=="float":
			yield (0,firstout)

	def iteritems(self):
		'''
		Does the exact same thing as above, but doesn't package things as the iter does.
		So, it preserves the structure of the input generator - if it doesn't have time, doensn't add
		time to it. 

		Parameters
		----------
		None

		Returns
		-------
		In order to proceed it, we need to do a next() on it!
		>>> def generator_without_time(stop=None):
				_=0
				while 1:
					yield (_+0.5)
					_+=1
		>>> obj2=SimulatedTimeSeries(generator_without_time())
		>>> obj2.iteritems() 
		0.5
		'''
		yield next(self.gen)

	def itertimes(self):
		'''
		Again as above, doesn't package things as the iter does.
		But, it doesn't preserve the structure of the input generator - it only returns the time, not value.
		even if the input has time, it returns only the value.

		IF the input doesn't have time, then it just returns a None.

		As all datasets have time,

		Parameters
		----------
		None

		Returns
		-------
		In order to proceed it, we need to do a next() on it!
		>>> def generator_without_time(stop=None):
				_=0
				while 1:
					yield (_+0.5)
					_+=1
		>>> obj2=SimulatedTimeSeries(generator_without_time())
		>>> obj2.iteritems() 
		None
		'''
		out=next(self.gen)
		if self.kind_of_input(out)=="TimedTuple":
			yield out[0]
		else:
			yield None

	def itervalues(self):
		'''
		Again as above, doesn't package things as the iter does.
		But, it doesn't preserve the structure of the input generator - it only returns the value, not time.
		Even if the input has time, it returns only the value.

		As all datasets have time,

		Parameters
		----------
		None

		Returns
		-------
		In order to proceed it, we need to do a next() on it!
		>>> def generator_with_time(stop=None):
				_=0
				while 1:
					yield (_+0.1,_+0.5)
					_+=1
		>>> obj2=SimulatedTimeSeries(generator_with_time())
		>>> obj2.iteritems() 
		0.5
		'''
		out=next(self.gen)
		if self.kind_of_input(out)=="TimedTuple":
			yield out[1]
		elif self.kind_of_input(out)=="UnTimedTuple":
			yield out[0]
		else:
			yield out


