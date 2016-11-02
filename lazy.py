class LazyOperation():
	"""
	LazyOperation function to lazily work with TimeSeries.

	Parameters
	----------
	This class takes a function, *args, and **kwargs as input.

	Returns
	-------
	A function of *args and **kwargs

	"""

	def __init__(self, function, *args, **kwargs):
		self._function = function
		self._args = args
		self._kwargs = kwargs

	def __str__(self):
		class_name = type(self).__name__        
		return "{} : Function = {}, Args = {}, Kwargs = {}".format(class_name, self._function, self._args, self._kwargs)

	def eval(self):
		# Recursively eval() lazy args
		new_args = [a.eval() if isinstance(a,LazyOperation) else a for a in self._args]
		new_kwargs = {k:v.eval() if isinstance(v,LazyOperation) else v for k,v in self._kwargs}
		#print("Self = ")
		#print(self)
		#print("Function = ")
		#print(self._function)
		#print("args = ")
		#print(self._args)
		return self._function(*new_args, **new_kwargs)

	def __len__(self):
		return len(self._args) 

def lazy(function):
	def create_thunk(*args, **kwargs):
		return LazyOperation(function, *args, **kwargs)
	return create_thunk

@lazy
def lazy_add(a,b):
	return a+b

@lazy
def lazy_mul(a,b):
	return a*b
