from WrappedDB import WrappedDB
import sys
import os
sys.path.append('../')
from TimeSeries import TimeSeries

os.remove("timeseriestest.dbdb")

t1 = [1.5, 2, 2.5, 3, 10.5]
v1 = [1, 3, 0, 1.5, 1]
z1 = TimeSeries(values=v1, times=t1)

t2 = [2]
v2 = [3]
z2 = TimeSeries(values=v2, times=t2)

db1 = WrappedDB("timeseriestest.dbdb", cacheSize=2)
db1.storeKeyAndTimeSeries(key="1", timeSeries=z1)
db1.storeKeyAndTimeSeries(key="2", timeSeries=z2)
db1.storeKeyAndTimeSeries(key="3", timeSeries=z1)
db1.getTimeSeries("3")
print(db1.cache)
db1.getTimeSeries("1")
print(db1.cache)
db1.getTimeSeries("1")
print(db1.cache)
db1.getTimeSeries("2")
print(db1.cache)
db1.getTimeSeries("2")
print(db1.cache)
 
del db1

# print(db1.getTimeSeries("1"))
# print(db1.getTimeSeries("2"))
# print(db1.getTimeSeriesSize("1"))
# print(db1.getTimeSeries("3"))


