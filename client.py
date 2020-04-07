

import os
from sys import exit, argv
import socket


# Command line checks 
if len(argv) < 2:
	print "USAGE python " + argv[0] + " <PORT>" 
	exit()


# Server (Address, Port)
server = ("localhost", int(argv[1]))


# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(server)

# Close connection
s.close();


print(server)


