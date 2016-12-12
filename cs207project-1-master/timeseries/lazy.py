class LazyOperation():
    """
    This is the thunk. It is used to isolate the function call from the function execution.
    It allows for lazy computations related to the time series.

    Attributes:
    -----------
    _function : python function
        this is the function to isolate the execution of until a future call
    args: float, int
        function args
    kwargs: float, int
        function kwargs
    """
    def __init__(self, function, *args, **kwargs):
        """
        Parameters:
        -----------
        function : python function 
            the function to use for the lazy operation

        Examples:
        ---------
        >>> 
        @lazy
        def lazy_add(a, b):
            return(a+b)
        >>> isinstance(lazy_add(2,4), LazyOperation)
        True
        """
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def eval(self):
        """
        Method to return the evaluation of the given instance of LazyOperation.

        Examples:
        ---------
        >>>
        @lazy
        def lazy_add(a,b):
            return (a+b)
        >>> lazy_add(41,1).eval()
        42
        """
        # Recursively eval() lazy args
        new_args = [a.eval() if isinstance(a,LazyOperation) else a for a in self._args]
        new_kwargs = {k:v.eval() if isinstance(v,LazyOperation) else v for k,v in self._kwargs.items()}

        return self._function(*new_args, **new_kwargs)

def lazy(function):
    """
        A lazy decorator to create a thunk/function - return a LazyOperation instance
    """
    def create_thunk(*args, **kwargs):
        return LazyOperation(function, *args, **kwargs)
    return create_thunk

"""
    lazy_add and a lazy_mul to be used to write tests for lazy.py.
"""
@lazy
def lazy_add(a,b):
    return a+b

@lazy
def lazy_mul(a,b):
    return a*b