import os, sys
sys.path.append('../')
import TimeSeries as ts
import SimilaritySearch as ss
import numpy as np
import random
import btreeDB as btreeDB
import shutil

def load_ts_data(file_name):
	"load timeseries data form given file name"
	ts_raw_data = np.loadtxt(file_name, delimiter=' ')
	ts_data = ts.TimeSeries(ts_raw_data[:,1], ts_raw_data[:,0])
	return ts_data

def	gen_vps(num):
	"generate vantage point"
	vp_indexes = random.sample(range(1000), num)
	vps_list = []
	for i in range(num):
		file_name = 'tsData/ts_data_'+str(vp_indexes[i])+'.txt'
		vp_ts = load_ts_data(file_name)
		std_vp_ts = ss.standardize(vp_ts)
		vps_list.append(std_vp_ts)
	return vps_list

def save_vp_dbs(num, vps_list):
	"save vantage point in btreeDB given in LAB10"
	for index in range(num):
		db_name = "vpDB/db_" + str(index) + ".dbdb"
		db = btreeDB.connect(db_name)
		for i in range(1000):
			file_name = 'tsData/ts_data_' + str(i) + '.txt'
			comp_ts = load_ts_data(file_name)
			std_comp_ts = ss.standardize(comp_ts)
			dis_to_vp = ss.kernel_dis(vps_list[index], std_comp_ts)
			db.set(dis_to_vp, file_name)
		db.commit()
		db.close()

def gen_dbs(num):
	"main function of generate vantage point database"
	if os.path.isdir('vpDB'):
		shutil.rmtree('vpDB')
	os.mkdir('vpDB')
	vps = gen_vps(num)
	save_vp_dbs(num, vps)

if __name__ == "__main__":
	gen_dbs(20)
