import socket

# Connect to server
server_name = 'localhost'
server_port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, server_port))

# Send commands to the server
command = input("Enter command (ls, get, put, quit): ")
client_socket.send(command.encode())

# Handle server responses and file transfers
# Your implementation for handling server responses and file transfers goes here

client_socket.close()
