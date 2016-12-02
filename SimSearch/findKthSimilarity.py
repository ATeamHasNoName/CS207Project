import sys
sys.path.append('../')
import TimeSeries as ts
import SimilaritySearch as ss
import numpy as np
import btreeDB


def load_ts_data(file_name):
    "load timeseries data form given file name"
    ts_raw_data = np.loadtxt(file_name, delimiter=' ')
    ts_data = ts.TimeSeries(ts_raw_data[:,1], ts_raw_data[:,0])
    return ts_data

def max_similarity_search(input_ts):
    """
    find the most similar vantage point of the target TS
    return tuple (minimum distance, vantage point, timeseries file name)
    """
    comp_ts = input_ts
    std_comp_ts = ss.standardize(comp_ts)
    min_dis = float('inf')
    min_db_name = ""
    min_ts_file_name = ""
    for i in range(20):
        db_name = "vpDB/db_" + str(i) + ".dbdb"
        db = btreeDB.connect(db_name)
        ts_data_file_name = db.get(0)
        vp_ts = load_ts_data(ts_data_file_name)
        std_vp_ts = ss.standardize(vp_ts)
        curr_dis = ss.kernel_dis(std_vp_ts, std_comp_ts)
        if min_dis > curr_dis:
            min_dis = curr_dis
            min_db_name = db_name
            min_ts_file_name = ts_data_file_name
    return min_dis, min_db_name, min_ts_file_name

def kth_similarity_search(input_ts, min_dis, min_db_name, k = 1):
    """
    find the most kth similar timeseries data
    return file names in an array
    """
    db = btreeDB.connect(min_db_name)
    keys, ts_file_names = db.get_smaller_nodes(2.0 * min_dis)
    ts_file_lens = len(ts_file_names)
    kth_ts_list = []
    for i in range(ts_file_lens):
        res_ts = load_ts_data(ts_file_names[i])
        std_res_ts = ss.standardize(res_ts)
        curr_dis = ss.kernel_dis(std_res_ts, input_ts)
        kth_ts_list.append((curr_dis, ts_file_names[i]))
    #sort in ascending order by distance
    kth_ts_list.sort(key=lambda kv: kv[0])
    #ill situation
    if(len(kth_ts_list) <= k):
        return kth_ts_list
    else:
        return kth_ts_list[: k]

def find_kth_similarity(input_file_name, k):
    """
    main function
    :param input_file_name: input TS file name to be compared
    :param k: top k similar nodes compared to input TS file
    :return: print the most kth similar timeseries file name
    """
    input_ts = load_ts_data(input_file_name)
    min_dis, min_db_name, min_ts_file_name = max_similarity_search(input_ts)
    kth_similarity_list = kth_similarity_search(input_ts, min_dis, min_db_name, k)
    print("The %dth closest TimeSeries data of %s is:" % (k, input_file_name))
    for i in range(len(kth_similarity_list)):
        print("No.%d %s" % (i + 1, kth_similarity_list[i][1]))

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    k = int(sys.argv[2])
    find_kth_similarity(input_file_name, k)
