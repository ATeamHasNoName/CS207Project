import sys
import threading
import socket
import select
import binascii
import time

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
                    value    = data[33 : 33 + length]

                    print("ts_or_id from client: %s" % (ts_or_id))
                    print("length from client: %s" % (length))
                    print("value from client: %s" %(value))
                    print(LINE)
                    # TODO: call functions with value and get results:

                    # If we have a connection then send data to the socket:
                    if SOCKETS[1]:
                        SOCKETS[1].send((value + "\n").encode())

                    # Remove socket from SOCKET list: 
                    SOCKETS.remove(SOCKETS[1])

                except:
                    continue


    #hostSocket.close()

def e(val):
    exit(val)

if __name__ == "__main__":
    sys.exit(Server())

