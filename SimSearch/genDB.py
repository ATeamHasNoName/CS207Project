import os, sys
import TimeSeries as ts
import SimilaritySearch as ss
import numpy as np
import btreeDB

if __name__ == "__main__":

	if os.path.isdir('vpDB'):
		pass
	else:
		os.mkdir('vpDB')

	vp_indexes = np.random.choice(1000,20, replace = False)
	vp_list= []

	for i in range(20):
		file_name = 'tsData/ts_data_'+str(vp_indexes[i])+'.txt'
		db_name = "vpDB/db_"+str(i)+".dbdb"
		ts_data = np.loadtxt(file_name, delimiter=' ')
		vp_ts = ts.TimeSeries(ts_data[:,0], ts_data[:,1])
		std_vp_ts = ss.stand(vp_ts, vp_ts.mean(), vp_ts.std())
		vp_list.append(std_vp_ts)

	for i in range(1000):
		file_name = 'tsData/ts_data_'+str(i)+'.txt'
		ts_data = np.loadtxt(file_name, delimiter=' ')
		comp_ts = ts.TimeSeries(ts_data[:,1], ts_data[:, 0])
		std_comp_ts = ss.stand(comp_ts, comp_ts.mean(), comp_ts.std())

		for j in range(20):
			db_name = "vpDB/db_"+str(j)+".dbdb"
			db = btreeDB.connect(db_name)
			dist = ss.kernel_corr(vp_list[j], std_comp_ts)

			db.set(dist, file_name)

			db.commit()
			db.close()