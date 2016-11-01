<<<<<<< HEAD
#from TimeSeries import TimeSeries

class LazyOperation():
=======
class LazyOperation():
    """
    LazyOperation function to lazily work with TimeSeries.

    Parameters
    ----------
    This class takes a function, *args, and **kwargs as input.

    Returns
    -------
    A function of *args and **kwargs

    >>> x = TimeSeries([1,2,3,4],[1,4,9,16])
    >>> print(x)
    >>> TimeSeries
    >>> Length: 4
    >>> First (oldest): 1, Last (newest): 4
    >>> y = x.lazy
    >>> print(y)
    >>> LazyOperation : Function = <class '__main__.TimeSeries'>, Args = ([1, 2, 3, 4], [1, 4, 9, 16]), Kwargs = {}
    >>> print(y.eval())
    >>> TimeSeries
    >>> Length: 4
    >>> First (oldest): 1, Last (newest): 4
    """


>>>>>>> 4bf8aaa73d857c7fc988e5a70dc78cfcfd667470
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
        #return self._function
        return self._function(*new_args, **new_kwargs)

<<<<<<< HEAD

=======
>>>>>>> 4bf8aaa73d857c7fc988e5a70dc78cfcfd667470
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


def main():
    thunk = check_length(TimeSeries(range(0,4),range(1,5)), TimeSeries(range(1,5),range(2,6)))
    print(thunk.eval())


    #x = TimeSeries([1,2,3,4],[1,4,9,16])
    #print(x) 
    #print(x.lazy.eval())

    #thunk = lazy_mul (1,2)
    #print(thunk.eval())
    #print(isinstance( lazy_add(1,2), LazyOperation ) == True)

if __name__ == "__main__":
	main()
