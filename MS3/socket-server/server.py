import sys
import threading
import socket
import select
import binascii

TIMEOUT = 30
SOCKETS = []
USERNAMES = []
BUFFERSIZE = 65536
ARGUMENTS = 3
PRINTUSERNAMESFREQUENCY = 60
LINE = "==================================================\n"

def ChatServer():
    
    if(len(sys.argv) < ARGUMENTS):
        print ('You typed in too few arguments.\n Please use the format: python server.py IP_ADDRESS PORT_NUMBER\n')
        e()
    
    # Get port number from input:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    
    # Set up host socket:
    hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind host socket and listen to other sockets:
    hostSocket.bind((HOST, PORT))
    hostSocket.listen(True)
    
    # Add host server to SOCKETS:
    SOCKETS.append(hostSocket)
    
    print ("A brand new server has fired up using port: " + str(PORT) + "!\n")
    
    # Listen to potential incoming sockets:
    while True:
        empty = []
        
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
                    p()
                    print("Server got an incoming request with data: %s\n" % (data))
                    # TODO:
                    # Calcualte stuff and get closest timeseries
                    ts_or_id = data[0]
                    length   = int(data[1:33]) # Length starts at character 1 and ends at 32
                    value    = data[33 : 33 + length]

                    print("ts_or_id from client: %s" % (ts_or_id))
                    print("length from client: %s" % (length))
                    print("value from client: %s" %(value))
                    p()
                    # TODO: call functions with value and get results:

                    # If we have a connection then send data to the socket:
                    if SOCKETS[1]:
                        SOCKETS[1].send((value + "\n").encode())

                    # Remove socket from SOCKET list: 
                    SOCKETS.remove(SOCKETS[1])

                except:
                    continue

    hostSocket.close()

def e():
    exit(0)

def p():
    print("========================================================================================\n");


def printUsernames():
    if (USERNAMES):
        uniqueUsernames = set(USERNAMES)
        print (LINE + "Connected users: " + ', '.join(uniqueUsernames))
        sys.stdout.write(LINE)
    threading.Timer(PRINTUSERNAMESFREQUENCY, printUsernames).start()

# Broadcast messages to all users expect the user that sent the message:
def broadcastMessage (hostSocket, incomingSocket, message):
    # Send the message only to other users:
    for socket in SOCKETS:
        if socket != hostSocket:
            try:
                socket.send(message)
            except:
                socket.close()

# And don't forget:
if __name__ == "__main__":
    sys.exit(ChatServer())
