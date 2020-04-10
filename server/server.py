

import socket
from threading import Thread
import traceback
import sys
import subprocess


# The port on which to listen
listenPort = 3000

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(4)


def process_get(clientSock, dataSock, *args):

	filename = args[0]

	try:
		file = open(filename, "rb")

		# This request can be succeeded
		clientSock.send(b"200 OK")

		while True:

			data = file.read(128)

			if not data:
				break

			dataSock.send(data)

		file.close()

	except FileNotFoundError:
		clientSock.send(b"500 Bad Request")
	except:
		clientSock.send(b"400 Server Error")




def process_list(clientSock, dataSock, *args):

	output = subprocess.check_output(["ls", "-l"]).decode()

	# This request can be succeeded
	clientSock.send(b"200 OK")

	print(output)

	dataSock.send(bytes(output, 'utf-8'))



def process_directive(clientSock, dataSock):
	msg, *args = clientSock.recv(128).decode().split()

	print(msg, *args)

	if msg == "GET":
		process_get(clientSock, dataSock, *args)
	elif msg == "LIST":
		process_list(clientSock, dataSock, *args)






def handleConnection(clientSock, address):

	print(f"Accepted connection from client {address}")
	
	while True:

		msg = clientSock.recv(32).decode()

		if not msg:
			break

		cmd, port, *args = msg.split()

		print(cmd, int(port), *args)

		if cmd == "OPEN":

			try:

				# Create a TCP socket
				dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				# Connect to the server
				dataSocket.connect((address[0], int(port)))

				process_directive(clientSock, dataSocket)

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
		
		# Accept connections
		clientSock, addr = welcomeSock.accept()

		Thread(target=handleConnection, args=(clientSock, addr)).start()

	except:
		break


print("Sutting down")
		
# Close our side
welcomeSock.close()
	

sys.exit();





