import sys
import socket
import getopt 
import threading
import subprocess
import argparse

def menu():
	parser = argparse.ArgumentParser(description='Python nc')
	parser.add_argument('-t', '--target', dest='target', metavar='TARGET_IP')
	parser.add_argument('-p', '--port', type=int, dest='port', metavar='TARGET_PORT')
	parser.add_argument('-l', '--listen', action='store_true', help='listen on [host]:[port] for incoming connections')
	parser.add_argument('-e', '--execute', metavar='EXECUTABLE', help='execute the given file upon receiving a connection')
	parser.add_argument('-c', '--command', action='store_true', help='initialize a command shell')
	parser.add_argument('-u', '--upload', metavar='DESTINATION', help='upon receiving connection upload a file and write to [destination]')
	return parser.parse_args()

def main():
	global args
	global listen 
	global target
	global port
	global upload
	global execute
	global command

	args 	= menu()
	listen 	= args.listen
	target 	= args.target
	port 	= args.port
	upload 	= args.upload
	execute = args.execute
	command = args.command

	if not listen and target is not None and port > 0:
		buffer = sys.stdin.read()
		client_sender(buffer)

	if listen:
		server_loop()

def client_sender(buffer):
	global target
	global port 

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:

		client.connect((target,port))

		if len(buffer):

			client.send(buffer)

			while True:

				recv_len = 1 
				response = ""

				while recv_len:

					data 	  = client.recv(4096)
					recv_len  = len(data)
					response += data

					if recv_len < 4096:
						break
					print response 

					buffer = raw_input("")
					buffer += "\n"

					client.send(buffer)
	except:

		print "[*] Exception! Exiting."
		
		client.close()


def server_loop(): 
	global target 
	global port 

	if target is None:
		target = "0.0.0.0"

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target,port))

	server.listen(5)

	print "[*] Listening on %s:%d" % (target,port)

	while True:
		client_socket, addr = server.accept()

		print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])

		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()

def run_command(command):

	command = command.rstrip()

	try: 
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except: 
		output = "Failed to execute command. \r\n"

	return output


def client_handler(client_socket):

	if upload is not None:

		file_buffer = ""

		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer += data

		try:
			file_descriptor = open(upload, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()

			client_socket.send("Successfully saved file to %s\r\n" % upload)


		except:
			client_socket.send("Failed to save file to %s\r\n" % upload)

	if execute is not None:
		output = run_command(execute)

		client_socket.send(output)

	if command: 

		while True:

			client_socket.send("<nc.py: #> ")

			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)

			response = run_command(cmd_buffer)

			client_socket.send(response)

	client_socket.close()

main()






