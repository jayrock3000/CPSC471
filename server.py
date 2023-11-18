import socket
import os
from Python.sendfile.sendfileserv import FileReceiverServer

# Set up socket
server_port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', server_port))
server_socket.listen(1)

print(f"FTP Server is ready on port {server_port}")

def show_listing():
    files = os.listdir('.')
    files = '\n'.join(files)

    return files

def send_file():
    # convert or make a duplicate of FileSender in sendfilecli.py
    # to send file from server
    pass


# Accept connections
while True:
    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    # Process client commands (e.g., ls, get, put, quit)
    while True:
        command = connection_socket.recv(1024).decode()

        # show files/directories in server
        if command == 'ls': show_listing()

        # send file from server
        elif command.startswith('get'): send_file()

        # Receive file
        elif command.startswith('put'):
            server_receive = FileReceiverServer(server_port)
            server_receive.start_server()
        else: 
            print("Error server-1: Unknown Command.")
            break
        # Example: if command == "quit": break

    connection_socket.close()
