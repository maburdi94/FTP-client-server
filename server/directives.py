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