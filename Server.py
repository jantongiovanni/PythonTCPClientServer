#
# Find_First_Client
#
from socket import *
import sys
import os
import logging
logger = logging.getLogger('ftpuploader')
import traceback
import time

serverPort = 12000
connAcceptedNum = 0;

# set number of clients to allow connection before termination
connLimit = 2

# a dictionary
# key: clientName
# value: tuple( connectionSocket, receivedAt, capMessage )
storage = {}

# to store capitalize message
capMessage = ''

# create TCP socket
with socket(AF_INET, SOCK_STREAM) as serverSocket:

    try:
        # assign IP address and port number to socket
        serverSocket.bind(('localhost' ,serverPort))

        # enable server to accept connections - to listen to connections
        # parameter: min 0 (default - if empty)
        # specifies the number of unaccepted connections that the system will allow
        # before refusing new connections
        # https://docs.python.org/3/library/socket.html
        # https://docs.python.org/2/library/socket.html
        serverSocket.listen(5)


        print('Server Ready')


        while True:

            # accepts a connection
            # severSocket must already by bound (bind) to address and listening
            # return values:
            # conn - new socket object usable to send/receive data on connection
            # address - address bound to the socket on the other end of connection i.e. ClientAddress
            connectionSocket, connectionAddress = serverSocket.accept()

            receivedAt = time.time()

            connAcceptedNum += 1

            # receive data from socket
            # return value:
            # a bytes object representing data
            # max amount to be received specified by buffer size
            content = connectionSocket.recv(2048).decode()

            # take message after semi colon and space from client
            # e.g. content = 'Client ' + argv[1] + ': ' + argv[2]
            msgIndex = content.find(':')
            message = content[(msgIndex + 1):]

            finding = 'Client'
            clientIndex = content.find(finding)
            clientName = content[ (clientIndex+ len(finding)): msgIndex ]

            print("Received from:" + clientName + " at " + time.asctime() )

            # capitalize message
            capMessage = message.upper()

            # print message to send to client
            print("Message for client: " + capMessage)

            # send message back to client
            connectionSocket.send(capMessage.encode())

            tupler = (connectionSocket, receivedAt, capMessage)

            storage[clientName] = tupler

            if connAcceptedNum >= connLimit :
                break

    except Exception as e :
        logger.error(str(e))
        traceback.print_exc()
        connectionSocket.close()
        sys.exit()

# prints the dictionary "storage"
# for k,v in storage.items() :
#     print( '\n' + k + ' at ' + str(v[1]) )
#     print('\n' + str(v[0]) )

# set the last clientName as starting point to compare receival time
compare = (storage.get(clientName))[1]

tempString = ''
temp2 = ''
temp1 = ''

# this is to find the client that made the first request
for k,v in storage.items() :

    if compare > v[1] :
        compare = v[1]
        tempString = k

# this is to form the acknowledgement message
for k,v in storage.items() :

    if tempString == k :
        # temp1 = 'Client ' + tempString + ': ' + '"' + v[2] + '"'
        temp1 = 'Client' + tempString
    else :
        # temp2 += ' Client ' + k + ': ' + '"' + v[2] + '"'
        temp2 += ' Client' + k

# concatenate acknowledgement message
ackMsg = temp1 + ' -RECEIVED BEFORE-' + temp2

# send acknowledgements to clients
for k,v in storage.items() :
    v[0].send(ackMsg.encode())
    print("Acknowledgement sent for " + k)

print("Connections closed")
connectionSocket.close()
