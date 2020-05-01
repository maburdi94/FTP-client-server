

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





def process_get(*tokens):

	# Create a TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind to random port
	s.bind((address,0))

	# Retrieve ephemeral port number
	port = s.getsockname()[1]

	# Start listening on the socket
	s.listen(1)

	# Ask server to connect for data transfer
	controlSocket.send(f"OPEN {port}\n\n".encode())
	status = controlSocket.recv(15).decode()

	print(status)
	if status == "200 OK":

		# Accept connections
		dataSock, addr = s.accept()

		filename = tokens[0][:32] 	# Trim to 32 Bytes according to spec.

		controlSocket.send(bytes("GET " + filename + "\n\n", 'utf-8'))

		msg = ""
		while True:

			data = dataSock.recv(1024).decode()

			if not data:
				break

			msg += data

		print(msg)

		dataSock.close()


def process_put(*tokens):
	print("PUT", *tokens)
	# Upload a file
	print("\nUploading file: {}...".format(filename))
	try:
		# Check the file exists
		content = open(filename, "rb")
	except:
		print("Couldn't open file. Make sure the file name was entered correctly.")
		return
	try:
		# Make upload request
		s.send("UPLD")
	except:
		print("Couldn't make server request. Make sure a connection has bene established.")
		return
	try:
		# Wait for server acknowledgement then send file details
		# Wait for server ok
		s.recv(BUFFER_SIZE)
		# Send file name size and file name
		s.send(struct.pack("h", sys.getsizeof(filename)))
		s.send(filename)
		# Wait for server ok then send file size
		s.recv(BUFFER_SIZE)
		s.send(struct.pack("i", os.path.getsize(filename)))
	except:
		print("Error sending file details")
	try:
		# Send the file in chunks defined by BUFFER_SIZE
		# Doing it this way allows for unlimited potential file sizes to be sent
		l = content.read(BUFFER_SIZE)
		print("\nSending...")
		while l:
			s.send(l)
			l = content.read(BUFFER_SIZE)
			content.close()
			# Get upload performance details
			upload_time = struct.unpack("f", s.recv(4))[0]
			upload_size = struct.unpack("i", s.recv(4))[0]
			print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(filename, upload_time, upload_size))
	except:
		print ("Error sending file")
		return
		# return

def process_list(*tokens):
	print("LIST", *tokens)

	# Create a TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind to random port
	s.bind((address,0))

	# Retrieve ephemeral port number
	port = s.getsockname()[1]

	# Start listening on the socket
	s.listen(1)

	# Ask server to connect for data transfer
	controlSocket.send(f"OPEN {port}\n\n".encode())
	status = controlSocket.recv(15).decode()

	print(status)

	if status == "200 OK":

		# Accept connections
		dataSock, addr = s.accept()

		controlSocket.send(bytes("LIST\n\n", 'utf-8'))

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



























