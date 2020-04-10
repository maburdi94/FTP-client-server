

import os
from sys import exit, argv
import socket
import argparse
from cmd import Cmd



# def process_get(*tokens):
# 	print("GET", *tokens)


# def process_ls(*tokens):
# 	print("LS", *tokens)


# def process_error(*tokens):
# 	print("ERROR", f"No command matched {tokens[0]} with arguments {tokens[1:]}")

#Sets up message's header by socket name and data. 
def set_data(socket_d, data):
    message = str(len(data))
    #data_size to be 10 
    while len(message) < 10:
        message = "0" + message

    data = message + data
    #Counter to keep track of data
    sent = 0

    #Sends all data
    while sent != len(data):
        sent += socket_d.send(data[sent:])
        

#Recieves data(bytes) from socket 
def get_data(socket_d, numBytes):
    #Buffers
    buffers = ""
    tmp = ""

    #Recives all the data
    while len(buffers) < numBytes:
        tmp =  socket_d.set_header(numBytes)
        if not tmp:
            break
        buffers += tmp
    #returns data recived
    return buffers

#Recives header to set up connection before getting the data
def set_header(socket_d):
    data = ""
    data_size = 0   
    buff = ""
    #Gets size of header
    buff = get_data(socket_d, 10)
    data_size = int(buff)
    #recives the header from socket 
    data = get_data(socket_d, data_size)
    #sends header name to recv_data
    return data

#TO set up FTP that handles commands of FTP     
class ftp_commands(Cmd):
    #To receive a file     
    def put(self, args):
        if len(args) > 0:
            msg = 'put'
            filename = args
            # send put to server
            set_data(client_socket, msg)
            tmp_port = int(set_header(client_socket))
            try:
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((server_name,tmp_port))
                set_data(data_socket, filename)
                print("Uploading file")
                while 1:
                    try:
                        file = open(filename, "r")
                    except:
                        print("problem opening the file", filename)
                    try:
                        #send at one byte at a time
                        bytesCount = 0
                        byte = file.read(1)
                        while byte != "":
                            set_data(data_socket, byte)
                            byte = file.read(1)
                            bytesCount += 1
                    finally:
                        file.close()
                        data_socket.close()
                        print("File Trasfer is complete: {} {}bytes".format(filename,bytesCount))
                        break
                        
            except socket.error as socketerror:
                print("Error: ", socketerror)


#setup arguements
port_number = argparse.ArgumentParser(description="FTP client side")
port_number.add_argument("server_name", help='Web address of server')
port_number.add_argument("port",  help="server port you wish to connecct to")
conn = port_number.parse_args()

# set up server name and port
server_name = conn.server_name
server_port= conn.port

# check for valid port
if server_port.isdigit():
    server_port = int(server_port)
else:
    print("The port {} is in the wrong format".format(server_port))
    sys.exit()

try:
    #set up socket
    print("Creating socket")
    client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    print("Connecting to server")
    client_socket.connect((server_name,server_port))

    print("Setting up FTP commands")
    prompt = ftp_commands()
    prompt.prompt = 'ftp> '
     # enable client input commands
    prompt.cmdloop('FTP connection established')
except socket.error as socketerror:
    print("FTP error: ", socketerror)

client_socket.close()
print("Command Socket Closed")

# # Command line checks 
# if len(argv) < 3:
#     print(f"USAGE python {argv[0]} <ADDRESS> <PORT>") 
#     exit()


# # Server (Address, Port)
# server = (argv[1], int(argv[2]))


# # Create a TCP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect to the server
# s.connect(server)
# print( "--------------------------------------------------------")
# print( "Connection success!")
# print(f"You are connected to {server[0]} on port {server[1]}.")
# print( "Type 'exit' to quit.")
# print( "--------------------------------------------------------")


# while True:

# 	cmd = input("ftp> ")

# 	if not cmd:
# 		continue

# 	if cmd == "exit":
# 		break

# 	cmd, *args = cmd.split()

# 	switch = {
# 		"GET": process_get,
# 		"PUT": process_put,
# 		"LS": process_ls
# 	}

# 	action = switch.get(cmd)

# 	if action:
# 		action(*args)
# 	else:
# 		process_error(cmd, *args)



# s.close()



























