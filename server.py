

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


def process_get(dataSock, *args):
	print("GET ", *args)

	try:
		
	except:
		print("File doesn't exist.")
		dataSock.send("500 Bad Request")



def process_list(dataSock, *args):
	print("LIST ", *args)

	output = subprocess.check_output(["ls", "-l"]).decode()

	print(output)

	dataSock.send(bytes(output, 'utf-8'))



def process_directive(clientSock, dataSock):
	print("Processing directive.")

	data = clientSock.recv(128).decode().split()

	print(f"Data: {data}")

	msg = data[0]

	if msg == "GET":
		process_get(dataSock, *data[1:])
	elif msg == "LIST":
		process_list(dataSock, *data[1:])






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

				print("Opening ", int(port))

				# Create a TCP socket
				dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				# Connect to the server
				dataSocket.connect((address[0], int(port)))

				print("Opened")

				# Let client know connection is open
				clientSock.send(b"200 OK")

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





