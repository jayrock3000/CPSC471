################################################################
# Group project for CPSC 471
# By Jeffrey Rhoten, Lucas Nguyen and Minh Gia Hoang
#
# Server.py
################################################################
# Import statements

import socket
import os
#from Python.sendfile.Receivefileserv import FileReceiverServer

# Debug mode provides additional console messages
debug = True

################################################################
# Function for ls command
# List all files on server

def getFileList():
    if debug == True:
        print("show_listing() function activated")
    
                        #### ATTENTION ####
                        
    # for future Minh, or for anyone gonna update this
    # Ensure we have a means to retrieve the precise location of the 'server_storage' folder.
    # Otherwise, it will only work on this (my laptop),
    # and upon installation on a new computer, the link/path MAY not work.
    directory = 'server_storage'

    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
        files = '\n- ' + '\n- '.join(files) + '\n'
        """
        print('writing directories list...')
        with open('server_response.txt', 'w') as f:
            f.write("Directory list: \n")
            f.write(files)
        f.close()
        print('done')
        """
        return files
        
    else:
        """
        with open('server_response.txt', 'w') as f:
            f.write("Directory not found or is not a directory.")
        f.close()
        # return "Directory not found or is not a directory."
        """
        return 'Directory not found'

################################################################
# Function for get command
# Send file to client

def sendFile():
    if debug == True:
        print("sendFile() function activated")

    print("WIP")

    # convert or make a duplicate of FileSender in sendfilecli.py
    # to send file from server
    pass

"""
################################################################
# Function for checking if requested file exists


#WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP

def findFile(fileName):
    if debug == True:
        print("findFile() function activated")

    directory = 'server_storage'
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
    
    print(files)
    if fileName in files:
        print("found it")

#WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP WIP

################################################################
# Determine the name of the file being requested

def parseFileName(command):
    if debug == True:
        print("parseFileName() function activated")
    pass
"""

################################################################
# Determine file size

def getFileSize(fileName):
    fileSize = 0

    return fileSize


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
        print("\n\nWaiting for connection...")
        
        # Accept connections
        connection_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}.\n\n")
        
        # Process client commands (e.g., ls, get, put, quit)
        while True:
            # Get command from client
            command = connection_socket.recv(1024).decode()
            if debug == True:
                print("command received:", end='')
                print(command)
            
            # Server sends acknowledgement
            ack = f"Server recieved: {command}"
            connection_socket.sendall(ack.encode('utf-8'))

            # Show files/directories in server
            if command == 'ls':
                # print('Raw Response from server:\n')
                files = getFileList()
                # print(dir_list)
                #print('Response sent to client')
                lsResponse = f"Directory list: \n {files}"
                connection_socket.sendall(lsResponse.encode('utf-8'))

            # Server sends file to client
            elif command.startswith('get'):
                
                sendFile()

            # Receive file
            # elif command.startswith('put'):
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