#
# Find_First_Client
# Cheryl Fong
# Joe Antongiovanni
#
from socket import *
import sys
import time
from datetime import datetime
import array

# needs 3 command line arguments
if len(sys.argv) != 3:
    print ('\nUsage:python3 Client.py "client-name" "message" \n')
    sys.exit()

# server side address and port number
#or 127.0.0.1
serverName = 'localhost'
serverPort = 12000

# create TCP socket/port to receive/send TCP packets
clientSocket = socket(AF_INET, SOCK_STREAM)

# set connection timeout
clientSocket.settimeout(10)

# connect to server's port
clientSocket.connect((serverName, serverPort))

content = 'Client ' + str(sys.argv[1]) + ': ' + str(sys.argv[2])

print(content)

# send encoded message from argument index 2
clientSocket.send(content.encode())

for x in range(2):
    try:

        # receive from server 2048 bytes as buffer
        receviedContent = clientSocket.recv(2048)

        print('Server says:  ' + receviedContent.decode())

    except Exception as e:

        print("Closing connection from Timeout")
        clientSocket.close()
        sys.exit()
