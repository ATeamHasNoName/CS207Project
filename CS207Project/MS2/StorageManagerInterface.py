import abc
class StorageManagerInterface(abc.ABC):
    """
    This is the interface for the Storage Manager class.
    """
        
    @abc.abstractmethod
    def store(self, id, t):
        """
        stores a instance of SizedContainerTimeSeriesInterface.
        """

    @abc.abstractmethod
    def size(self, id):
        """
        fetches the size of the SizedContainerTimeSeriesInterface and returns it.
        """

    @abc.abstractmethod
    def get(self, id):
        """
        returns a instance of SizedContainerTimeSeriesInterface instance.
        """
