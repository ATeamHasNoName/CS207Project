from WrappedDB import WrappedDB
import sys
sys.path.append('../')
from TimeSeries import TimeSeries

t1 = [1.5, 2, 2.5, 3, 10.5]
v1 = [1, 3, 0, 1.5, 1]
z1 = TimeSeries(values=v1, times=t1)

t2 = [2]
v2 = [3]
z2 = TimeSeries(values=v2, times=t2)

db1 = WrappedDB("exampleDB.dbdb")
db1.storeKeyAndTimeSeries("1", z1)
db1.storeKeyAndTimeSeries("2", z2)
print(db1.getTimeSeries("1"))
print(db1.getTimeSeries("2"))