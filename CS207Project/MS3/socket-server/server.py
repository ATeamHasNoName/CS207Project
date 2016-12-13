import sys
import json
import threading
import socket
import select
import binascii
import time
import numpy as np
from Distance_from_known_ts import Simsearch
sys.path.append('../')
from TSDBSerialize import Serialize
sys.path.append('../MS1/')
from TimeSeries import TimeSeries
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface


TIMEOUT = 30
SOCKETS = []
BUFFERSIZE = 65536  # TODO: Increase??
ARGUMENTS = 3
LINE = "========================================================================\n"

def Server():
    
    if(len(sys.argv) < ARGUMENTS):
        print ('You typed in too few arguments.\n Please use the format: python server.py IP_ADDRESS PORT_NUMBER\n')
        e(2)
    
    # Get port number from input:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    
    TEST = 0
    if sys.argv[3]:
        TEST = int(sys.argv[3])
    # Set up host socket:
    hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind host socket and listen to other sockets:
    hostSocket.bind((HOST, PORT))
    hostSocket.listen(True)
    
    # Add host server to SOCKETS:
    SOCKETS.append(hostSocket)
    
    print ("A brand new server has fired up using port: " + str(PORT) + "!\n")

    # First time server is started: Fill the database with dummy data:
    SS = Simsearch(load_ts_file("169975.dat_folded.txt"), 5)

    wait_count = 0
    # Listen to potential incoming sockets:
    while True:
        empty = []

        # Used for testing purposes:
        if TEST > 0:
            wait_count += 1        
        if (TEST > 0 and wait_count == 100000):
           e(0)

        # Fetch incoming sockets:
        incomingSockets,w,err = select.select(SOCKETS,empty,empty,0)

        for incomingSocket in incomingSockets:
            # A new client has initiated a connection:
            if incomingSocket == hostSocket:
                d,_ = hostSocket.accept()
                SOCKETS.append(d)

            # Message from user received:
            else:
                try:
                    # Fetch data from the incoming socket:
                    data = incomingSocket.recv(BUFFERSIZE)
                    data = data.decode('utf-8')

                    print(LINE)
                    print("Server got an incoming request with data: %s\n" % (data))
                    ts_or_id = data[0]
                    length   = int(data[1:33]) # Length starts at character 1 and ends at 32
                    ts_bytes    = data[33 : 33 + length]
                    ts_bytes = bytes(ts_bytes, encoding='utf-8')
                    print("ts_or_id from client: %s" % (ts_or_id))
                    print("length from client: %s" % (length))
                    print("ts_bytes from client: %s" %(ts_bytes))
                    print(LINE)
                    if int(ts_or_id) == 1:
                        # Fetch TS:
                        # Convert bytes to json
                        print("inside ts_or_id")
                        ts_json = Serialize().bytes_to_json(ts_bytes)
                        #ts_json = json.loads(bytes_to_json.decode('utf-8'))
                        print("After byees to json")
                        print(ts_json)
                        # Convert json to ts:
                        print("Before json to ts")
                        ts = Serialize().json_to_ts(ts_json)
                        print("After json to ts")
                        print("Got TS:")
                        print(ts)
                        top_5_ts = Simsearch(ts, 5)
                        print("Top 5 ts:")
                        print(top_5_ts)

                        

                    # If we have a connection then send data to the socket:
                    if SOCKETS[1]:
                        SOCKETS[1].send((top_5_ts + "\n").encode())

                    # Remove socket from SOCKET list: 
                    SOCKETS.remove(SOCKETS[1])

                except:
                    continue


    #hostSocket.close()
def load_ts_file(filepath):
    '''
    Takes in file and reads time series from it

	Parameters
	----------
	filepath: path of the file 
	
	Returns
	-------
	timeSeries object : TimeSeries class

	>>> ts=load_ts_file('input.txt')
	>>> ts.values()[0]
	15.137
    '''
    
    #Only considers the first two columns of the text file (other columns are discarded)
    #Only evaluates time values between 0 and 1
    #First column is presumed to be times and second column is presumed to be light curve values.
    data = np.loadtxt(filepath, delimiter=' ',dtype = str)
    clean_input = []
    for i in range(len(data)):
        row = data[i].split("\\t")
        clean_input.append([float(row[0][2:]),float(row[1])])
    data = np.array(clean_input)

    _ , indices = np.unique(data[:, 0], return_index=True)

    data = data[indices, :]
    times, values = data.T
    full_ts = TimeSeries(times=list(times),values=list(values))
    interpolated_ts = full_ts.interpolate(list(np.arange(0.0, 1.0, (1.0 /100))))
    full_ts_interpolated = TimeSeries(times=list(np.arange(0.0, 1.0, (1.0 /100))),values=list(interpolated_ts))
    return full_ts_interpolated

def e(val):
    exit(val)

if __name__ == "__main__":
    sys.exit(Server())

