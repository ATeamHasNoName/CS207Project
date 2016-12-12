
import random
import os
import sys
import operator
from WrappedDB import WrappedDB

sys.path.append("../")
from FileStorageManager import FileStorageManager

sys.path.append('../MS1/')
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from TimeSeries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries

# wdb = WrappedDB()
# ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
# key = wdb.storeKeyAndTimeSeries(key="1", timeSeries=ts) # Check to see if there is a file created
# print(wdb.getTimeSeries(1))

fsm = FileStorageManager()
# os.remove("ts_2.dbdb")
ts = TimeSeries(values=[0, 2, -1, 0.5, 0], times=[1, 1.5, 2, 2.5, 10])
key = fsm.store(ts)
print(fsm.get(key).values())
print("returned key: ", key)