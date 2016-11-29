import os, sys
import TimeSeries as ts
import SimilaritySearch as ss
import numpy as np

if __name__ == "__main__":

    if os.path.isdir('tsData'):
        pass
    else:
        os.mkdir('tsData')

    for i in range(1000):
        file_name = 'tsData/ts_data_'+str(i)+'.txt'
        f = open(file_name,'w+')
        t1 = ss.tsmaker(0.5, 0.1, 0.01)
        np.savetxt(file_name,np.transpose(np.array([list(t1.itertimes()),list(t1)])), delimiter=' ')
        f.close()
