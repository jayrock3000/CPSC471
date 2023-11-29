################################################################
# Group project for CPSC 471
# By Jeffrey Rhoten, Lucas Nguyen and Minh Gia Hoang
#
# Server.py
################################################################
# Import statements

import socket
import os
from Python.sendfile.sendfileserv import FileReceiverServer
import pickle

# Debug mode provides additional console messages
debug = True

################################################################
# Function for ls command
# List all files on server

def show_listing():
    ################################################## original code

    if debug == True:
        print("show_listing() function activated")
    
    #files = os.listdir('.')
    #files = '\n'.join(files)

    #return files
    ##################################################

    #get current working directory and get folder path
    cwd = os.getcwd()
    stored = os.path.join(cwd, "stored")

    # check if the stored folder exists
    if os.path.exists(stored):
        # get the list of files in the stored folder
        files_list = os.listdir(stored)
        # return the list of files
        return files_list
    else:
        # return an empty list if the stored folder does not exist
        return []


################################################################
# Function for get command
# Send file to client

def send_file():
    if debug == True:
        print("send_file() function activated")
    # convert or make a duplicate of FileSender in sendfilecli.py
    # to send file from server
    pass

################################################################
# Main Method

def main():

    # Set up socket
    server_port = 5432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', server_port))
    server_socket.listen(1)

    print(f"FTP Server is ready on port {server_port}")

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

            # Show files/directories in server
            if command == 'ls':
                print("WIP")
                list = show_listing()
                sendData = pickle.dumps (list)
                #send user list
                print("sending list")
                connection_socket.send(sendData.encode())

            # send file from server
            elif command.startswith('get'):
                print("WIP")
                #send_file()

            # Receive file
            elif command.startswith('put'):
                print("WIP")
                #server_receive = FileReceiverServer(server_port)
                #server_receive.start_server()

            # Close if 'quit' received
            elif command == 'quit':
                connection_socket.close()
                print("server socket has closed")
                print("server has quit")
                exit()

            # Handle exceptions
            else: 
                print("Error server-1: Unknown Command.")
                break

            connection_socket.close()
            print("server socket has closed")
            break

################################################################
# Run main when program starts

if __name__ == "__main__":
    main()

#END