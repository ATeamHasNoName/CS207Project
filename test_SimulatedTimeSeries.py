import numpy as numpy
from random import normalvariate, random
from itertools import count
from SimulatedTimeSeries import SimulatedTimeSeries

######Defining the generators to be used for testing the SimulatedTimeSeries Class#########3
def generator_with_time(stop=None):
	_=0
	while 1:
		yield (_+0.1,_+0.5)
		_+=1

def generator_without_time(stop=None):
	_=0
	while 1:
		yield _+0.5
		_+=1

def generator_without_time_tuple(stop=None):
	_=0
	while 1:
		yield (_+0.5,)
		_+=1

############# SET UP####################################
def setUp():
	Obj_with_time=SimulatedTimeSeries(generator_with_time())
	Obj_without_time=SimulatedTimeSeries(generator_without_time())
	Obj_without_time_tuple=SimulatedTimeSeries(generator_without_time_tuple())
	return (Obj_with_time,Obj_without_time,Obj_without_time_tuple)

(obj1,obj2,obj3)=setUp()

data1=next(obj1.produce(chunk=8))
data2=next(obj2.produce(chunk=8))
data3=next(obj3.produce(chunk=8))
#print(data3)
#############################TESTING INITATION AND PRODUCE FUNCTION################################################
def test_init_with_time_check_time():
	assert data1[0][0]==2.1
def test_init_with_time_check_value():
	assert data1[0][1]==2.5

def test_init_without_time_check_time():
	assert data2[0][0]==0
def test_init_without_time_check_value():
	assert data2[0][1]==2.5

def test_init_without_time_tuple_check_time():
	assert data3[0][0]==0
def test_init_without_time_tuple_check_value():
	assert data3[0][1]==2.5
############# TESTING ITER ######################
def test_iter_with_time():
	for a in obj1:
		assert a==(10.1, 10.5)
def test_iter_without_time():
	for a in obj2:
		assert a==(0,10.5)
def test_iter_without_time_tuple():
	for a in obj3:
		assert a==(0,10.5)
############# TESTING ITERITEMS ######################
def test_iteritems_with_time():
	assert next(obj1.iteritems()) == (11.1,11.5)
def test_iteritems_without_time():
	assert next(obj2.iteritems()) == 11.5
def test_iteritems_without_time_tuple():
	assert next(obj3.iteritems()) == (11.5,)
############# TESTING ITERTIMES ######################

def test_itertimes_with_time():
	assert next(obj1.itertimes())==12.1
def test_itertimes_without_time():
	assert next(obj2.itertimes())==None
def test_itertimes_without_time_tuple():
	assert next(obj3.itertimes())==None
############# TESTING ITERVALUES ######################

def test_itervalues_with_time():
	assert next(obj1.itervalues())==13.5
def test_itervalues_without_time():
	assert next(obj2.itervalues())==13.5
def test_itervalues_without_time_tuple():
	assert next(obj3.itervalues())==13.5

##############################TESTING TEARDOWN#########################
(obj7,obj8,obj9)=setUp()
del obj7
def deleted_object():
	try: 
		obj7
	except:
		return "Doesn't exist"
def check_deleted():
	assert deleted_object()=="Doesn't exist"
check_deleted()
