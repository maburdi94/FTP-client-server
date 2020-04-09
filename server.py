import socket
import sys
import argparse
import commands
import os

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
    
#Sets up and creates an obeject with an accepted connection
def data_connection():
    socket_s = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
    #Open the connection
    socket_s.bind(('',0))
    socket_number = str(socket_s.getsockname()[1])
    set_data(connection_socket,  socket_number)
    socket_s.listen(1)
    new_socket ,addr = socket_s.accept()
    return new_socket


#--------------------------Program Begins---------------------------
#Get the port number
port_number = argparse.ArgumentParser(description="Server Starts")
port_number.add_argument("port",  help="server port to start")
conn = port_number.parse_args()
server_conn = conn.port

#Checks if it's valid or not
if server_conn.isdigit():
    server_conn = int(server_conn)
else:
    print("The port {} is not accepted".format(server_conn))
    sys.exit()

#Initialize the socket    
server_socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
server_socket.bind(('',server_conn))

#listens for one connection on the network
server_socket.listen(1)
print ('Server is running...')
connection_socket ,addr = server_socket.accept()
print ('Connected by', addr)
data =''

#Wait for commands ls out 
connection_socket.close()
print("Command Socket is closed")
