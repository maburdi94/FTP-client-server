

import os
from sys import exit, argv
import socket




# Command line checks 
if len(argv) < 3:
	print(f"USAGE python {argv[0]} <ADDRESS> <PORT>") 
	exit()


# Server (Address, Port)
address, controlPort = (argv[1], int(argv[2]))

# Create a TCP socket
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
controlSocket.connect((address, controlPort))




def get_data_socket(sock, address):
	# Create a TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind to random port
	s.bind((address,0))

	# Retrieve ephemeral port number
	port = s.getsockname()[1]

	# Start listening on the socket
	s.listen(1)

	# Ask server to connect for data transfer
	sock.send(f"OPEN {port}\n\n".encode())

	# Accept connections
	return s.accept()



def process_get(filename="", newFilename="", *args):

	if not filename:
		print(f"Usage:\n\t GET <FILENAME> [<NEW_FILENAME>]") 
		return

	# Accept connections
	dataSock, addr = get_data_socket(controlSocket, address);

	# Send GET message
	controlSocket.send(bytes("GET " + filename + "\n\n", 'utf-8'))

	# Check server status
	status = controlSocket.recv(24).decode()

	print(status)

	if status == "200 OK":

		try:
			file = open(newFilename if newFilename else filename, "w")

			while True:

				data = dataSock.recv(1024).decode()

				if not data:
					break

				file.write(data)

			print("File downloaded successfully.")
		except Exception as e:
			print("File not downloaded successfully. \n", e)
		finally:
			file.close()
	
	dataSock.close()


def process_put(*tokens):
	print("PUT", *tokens)


def process_list(*tokens):

	dataSock, addr = get_data_socket(controlSocket, address);

	controlSocket.send(bytes("LIST\n\n", 'utf-8'))

	status = controlSocket.recv(24).decode()

	print(status)

	if status == "200 OK":

		msg = ""
		while True:

			data = dataSock.recv(1024).decode()

			if not data:
				break

			msg += data

		print(msg)

		dataSock.close()


def process_error(*tokens):
	print("ERROR", f"No command matched {tokens[0]} with arguments {tokens[1:]}")







print( "--------------------------------------------------------")
print( "Connection success!")
print(f"You are connected to {address} on port {controlPort}.\n")
print("Enter one of the following commands:")
print("  GET <filename>")
print("  PUT <filename>")
print("  LIST")
print( "Or type 'exit' to quit.")
print( "--------------------------------------------------------")


options = {
	"GET": process_get,
	"PUT": process_put,
	"LIST": process_list
}


while True:

	cmd = input("ftp> ").lower()

	if not cmd:
		continue

	if cmd == "exit":
		break

	cmd, *args = cmd.split()

	action = options.get(cmd.upper())

	if action:
		action(*args)
	else:
		process_error(cmd, *args)
		continue





controlSocket.close()



























