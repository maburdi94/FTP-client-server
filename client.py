

import os
from sys import exit, argv
import socket



def process_get(*tokens):
	print("GET", *tokens)


def process_put(*tokens):
	print("PUT", *tokens)


def process_ls(*tokens):
	print("LS", *tokens)


def process_error(*tokens):
	print("ERROR", f"No command matched {tokens[0]} with arguments {tokens[1:]}")



# Command line checks 
if len(argv) < 3:
	print(f"USAGE python {argv[0]} <ADDRESS> <PORT>") 
	exit()


# Server (Address, Port)
server = (argv[1], int(argv[2]))


# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect(server)

print( "--------------------------------------------------------")
print( "Connection success!")
print(f"You are connected to {server[0]} on port {server[1]}.")
print( "Type 'exit' to quit.")
print( "--------------------------------------------------------")


while True:

	cmd = input("ftp> ")

	if not cmd:
		continue

	if cmd == "exit":
		break

	cmd, *args = cmd.split()

	switch = {
		"GET": process_get,
		"PUT": process_put,
		"LS": process_ls
	}

	action = switch.get(cmd)

	if action:
		action(*args)
	else:
		process_error(cmd, *args)



s.close()



























