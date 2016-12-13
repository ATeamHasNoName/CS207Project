import abc

class StorageManagerInterface(metaclass=abc.ABCMeta):
	"""
    Description
    -----------
    Abstract Base Class for storage manager implementations.
    """

	@abc.abstractmethod
	def store (self, id, t):
		"""
	    Description
	    -----------
		Method used to store a time series using the storage manager. 

	    Parameters
	    ----------
	    self: Instance of subclass of StorageManagerInterface.

	    id : int
	    	Used as an identification of a particular time series being stored.

	    t : SizedContainerTimeSeriesInterface
	    	A time series associated with SizedContainerTimeSeriesInterface 
	    	that allows for time series data persistence.

	    Returns
	    -------
	    SizedContainerTimeSeriesInterface
	    """

	@abc.abstractmethod
	def size(self, id):
		"""
	    Description
	    -----------
	    Method used to return the size of a particular time series stored based on the 
	    provided id.

	    Parameters
	    ----------
	    self: Instance of subclass of StorageManagerInterface.

	    id : int
	    	The id of the time series of interest.

	    Returns
	    -------
	    int : the size of the time series in question.
	    """

	@abc.abstractmethod
	def get(self, id):
		"""
	    Description
	    -----------
	    Method used to return a particular time series stored based on the 
	    provided id.

	    Parameters
	    ----------
	    self: Instance of subclass of StorageManagerInterface.

	    id : int
	    	The id of the time series of interest.

	    Returns
	    -------
	    SizedContainerTimeSeriesInterface : the time series data requested by id.
	    """