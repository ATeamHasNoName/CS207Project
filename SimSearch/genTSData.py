import os, sys
sys.path.append('../')
import SimilaritySearch as ss
import numpy as np
import shutil

def gen_ts_data(num):
    "generate given number of random timeseries data"
    if os.path.isdir('tsData'):
        shutil.rmtree('tsData')
    os.mkdir('tsData')
    for i in range(num):
        file_name = 'tsData/ts_data_'+str(i)+'.txt'
        f = open(file_name,'w+')
        t1 = ss.tsmaker(0.5, 0.1, 0.01)
        np.savetxt(file_name,np.transpose(np.array([list(t1.itertimes()),list(t1)])), delimiter=' ')
        f.close()
    return

if __name__ == "__main__":
    gen_ts_data(1000)
