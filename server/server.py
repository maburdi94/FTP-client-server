

import socket
from threading import Thread
import traceback
import sys
import subprocess

# Module with ftp directive definitions
import diretives


# The port on which to listen
listenPort = 3000

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(4)





def handleConnection(clientSock, address):

	print(f"Accepted connection from client {address}")
	
	while True:

		msg = clientSock.recv(32).decode()

		if not msg:
			break

		# OPEN <port>
		cmd, port, *args = msg.split()

		#  Client requested data transfer on port <port>
		if cmd == "OPEN" and port:

			try:

				# Set up a TCP connection socket for the transfer
				dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				# And connect to the client on the requested port number
				dataSocket.connect((address[0], int(port)))


				# Listen for incoming commands on the client socket
				# (This will pause program execution at this line)
				msg, *args = clientSock.recv(128).decode().split()


				# Use the appropriate handler for the command received

				# Process GET request
				if msg == "GET":
					process_get(clientSock, dataSock, *args)

				# Process LIST request
				elif msg == "LIST":
					process_list(clientSock, dataSock, *args)


			except Exception as e:
				print(e)

			finally:
				dataSocket.close()


	print(f"Disconnect connection on {address}")
	clientSock.close()





		
# Accept connections forever
while True:
	
	print("Waiting for connections...")

	try:
		
		# Accept connections on welcome socket
		clientSock, addr = welcomeSock.accept()

		# Open a new running thread for the client socket
		Thread(target=handleConnection, args=(clientSock, addr)).start()

	except:
		break



print("Sutting down")
		
# Close our side
welcomeSock.close()
	

sys.exit();





