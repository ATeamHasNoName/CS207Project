import sys
import string
import select
import socket
import signal
import json
import numpy as np
from Distance_from_known_ts import Simsearch
sys.path.append("../")
from TSDBSerialize import Serialize
sys.path.append('../MS1/')
from TimeSeries import TimeSeries
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface



ARGUMENTS = 5
BUFFERSIZE = 65536
TIMEOUTLENGTH = 3

def Client():

    if(len(sys.argv) < ARGUMENTS):
        print ('You typed in too few arguments.\n Please use the format: python client.py IP_ADDRESS PORT_NUMBER TS_OR_ID VALUE\n')
        return 2

    host, port, ts_or_id, filename = readCommandLine()

    # Get text as TimeSeries from file:
    ts_text = load_ts_file(filename)

    # Convert TimeSeries text to json:
    ts_json = Serialize().json_to_jsonstring(Serialize().ts_to_json(ts_text))

    # Set up socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.settimeout(TIMEOUTLENGTH)

    # Try to connect to the server:
    try :
        #print("Connecting to IP: %s" % (host))
        #print("Connecting to port: %s\n" % (port))
        s.connect((host, port))
    except :
        print( 'Cannot connect to the server. IP address provided or port number might be wrong or host is not up.\n')
        return 3

    ts_to_json_LengthBinary = binaryLength32(len(ts_json))
    # Format sent to server is:
    # 0/1: id is 0, ts is 1        [Starts at byte number 1]
    # length of id / ts in 32 bits [Starts at byte number 2]
    # value of id or ts            [Starts at byte number 34]
    sendTsOrIdToServer = ts_or_id + ts_to_json_LengthBinary + ts_json

    #if (int(ts_or_id) == 0):
        #print("Sending id to server")
    #else:
        #print("Sending TimeSeries to server")

    s.send(Serialize().jsonstring_to_bytes(sendTsOrIdToServer))
    #print("Data is encoded as: %s\n" % (bytes(sendTsOrIdToServer, encoding='utf-8')))

    while True:
        empty = []
    
        # Fetch sockets from server:
        availableSockets = [sys.stdin, s]
        sockets,write,error = select.select(availableSockets,empty,empty)

        for incomingSocket in sockets:
            if incomingSocket == s:
                buffer = incomingSocket.recv(BUFFERSIZE)
                buffer = buffer.decode()
                sys.stdout.write(str(buffer))
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                sys.exit()

def readCommandLine():
    host = sys.argv[1]
    port = int(sys.argv[2])
    ts_or_id = sys.argv[3]
    filename = str(sys.argv[4])
    return host, port, ts_or_id, filename

def binaryLength32(length):
    '''
    Returns the binary length of string.

	Parameters
	----------
	length: the length of the string 
	
	Returns
	-------
	the length of the string in 32 bit binary

	>>> st = "CS207"
	>>> st_length = len(st)
	>>> st_binary_length = binaryLength32(st_length)
	>>> st_binary_length
	'00000000000000000000000000000101'
    '''
    return format(length, '032b')

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


if __name__ == "__main__":
    exit(Client())
