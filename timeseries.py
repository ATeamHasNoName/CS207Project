import itertools
import reprlib

class TimeSeries:

    # Data is a sequence that is required, but can be zero-length
    def __init__(self, data = []):
        self._timeseries = list(data)

    def __len__(self):
        return len(self._timeseries)

    def __getitem__(self, key):
        if key >= self.__len__():
            raise IndexError('Index chosen is out of range.')
        return self._timeseries[key]

    def __setitem__(self, key, value):
        if key >= self.__len__():
            raise IndexError('Index chosen is out of range.')
        self._timeseries[key] = value

    def __repr__(self):
        class_name = type(self).__name__
        myrepr = reprlib.aRepr
        myrepr.maxlist = 100 # More than 100 then replace with ellipses
        components = myrepr.repr(self._timeseries)
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)   
    
    def __str__(self):
        # Shows the length and the first and last elements
        class_name = type(self).__name__
        first = 'N/A'
        last = 'N/A'
        if len(self._timeseries) > 0:
            first = str(self._timeseries[0])
            last = str(self._timeseries[-1])
        return '%s\nLength: %d\nFirst: %s, Last: %s' % (class_name, len(self._timeseries), first, last)
    