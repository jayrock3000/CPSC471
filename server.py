import socket
import os
from Python.sendfile.sendfileserv import FileReceiverServer

# Variable for debugging program
debug = True

# Set up socket
server_port = 5432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', server_port))
server_socket.listen(1)

print(f"FTP Server is ready on port {server_port}")

def show_listing():
    if debug == True:
        print("show_listing() function activated")
    
    files = os.listdir('.')
    files = '\n'.join(files)

    return files

def send_file():
    if debug == True:
        print("send_file() function activated")
    # convert or make a duplicate of FileSender in sendfilecli.py
    # to send file from server
    pass



# Establish connection
while True:
    print("Waiting for connection...")
    
    # Accept connections
    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    
    # Process client commands (e.g., ls, get, put, quit)
    while True:
        # Get command from client
        command = connection_socket.recv(1024).decode()
        if debug == True:
            print("command received:", end='')
            print(command)

        # show files/directories in server
        if command == 'ls': show_listing()

        # send file from server
        elif command.startswith('get'): send_file()

        # Receive file
        elif command.startswith('put'):
            server_receive = FileReceiverServer(server_port)
            server_receive.start_server()

        elif command == 'quit':
            connection_socket.close()
            print("server socket has closed")
            print("server has quit")
            exit()

        else: 
            print("Error server-1: Unknown Command.")
            break

        connection_socket.close()
        if debug == True:
            print("server socket has closed")
        break