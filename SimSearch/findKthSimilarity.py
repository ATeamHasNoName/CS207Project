import os, sys
import TimeSeries as ts
import SimilaritySearch as ss
import numpy as np
import random
import btreeDB

def load_ts_data(file_name):
	ts_raw_data = np.loadtxt(file_name, delimiter=' ')
	ts_data = ts.TimeSeries(ts_raw_data[:,1], ts_raw_data[:,0])
	return ts_data

def load_input_ts_data(file_name):
    ts_data = np.loadtxt(file_name, delimiter=' ')
    comp_ts = ts.TimeSeries(ts_data[:, 1], ts_data[:, 0])
    return comp_ts

def max_similarity_search(input_ts):
    comp_ts = input_ts
    std_comp_ts = ss.standarize(comp_ts)

    min_dis = float('inf')
    min_db_name = ""
    min_ts_file_name = ""
    for i in range(20):
        db_name = "vpDB/db_" + str(i) + ".dbdb"
        db = btreeDB.connect(db_name)
        ts_data_file_name = db.get(0)
        vp_ts = load_ts_data(ts_data_file_name)
        std_vp_ts = ss.standarize(vp_ts)
        curr_dis = ss.kernel_dis(std_vp_ts, std_comp_ts)
        #print(curr_dis)
        if min_dis > curr_dis:
            min_dis = curr_dis
            min_db_name = db_name
            min_ts_file_name = ts_data_file_name
    #print(min_dis)
    #print(min_ts_file_name)
    return min_dis, min_db_name, min_ts_file_name

def kth_similarity_search(input_ts, min_dis, min_db_name, k = 1):
    db = btreeDB.connect(min_db_name)
    keys, ts_file_names = db.get_smaller_nodes(2.0 * min_dis)
    ts_file_lens = len(ts_file_names)
    print(ts_file_lens)
    kth_ts_list = []
    for i in range(ts_file_lens):
        res_ts = load_ts_data(ts_file_names[i])
        std_res_ts = ss.standarize(res_ts)
        curr_dis = ss.kernel_dis(std_res_ts, input_ts)
        kth_ts_list.append((curr_dis, ts_file_names[i]))
    kth_ts_list.sort(key=lambda kv: kv[0])
    if(len(kth_ts_list) < k):
        return kth_ts_list
    else:
        return kth_ts_list[: k]


if __name__ == "__main__":

    input_ts_file_name = "ts_data_1.txt"
    input_ts= load_input_ts_data(input_ts_file_name)
    a, b, c = max_similarity_search(input_ts)
    d = kth_similarity_search(input_ts, a, b, 10)
    print(len(d))