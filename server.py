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
        print("getFileList() function activated")
    
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


################################################################
# Function for checking if requested file exists

def fileExists(fileName):
    if debug == True:
        print("fileExists() function activated")

    directory = 'server_storage'
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
    
    #print(files)
    if fileName in files:
        return True
    
    return False


################################################################
# Determine the name of the file being requested

def parseFileName(command):
    if debug == True:
        print("parseFileName() function activated")
    
    # Remove get from commmand
    fileName = command.removeprefix('get ')

    if debug == True:
        print("fileName: " + fileName)

    return fileName

################################################################
# Send file to client (Data channel for GET)
def dataSocket(fileName):
    if debug == True:
        print("dataSocket() function activated")

    # Connect to server
    receiverName = 'localhost'
    receiverPort = 5433

    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((receiverName, receiverPort))

    fileName = "server_storage/" + fileName

    fileObj = open(fileName, "r")
    numSent = 0
    fileData = None

    # Send until all data is sent
    while True:
        fileData = fileObj.read(65536)

        if fileData:
            dataSizeStr = str(len(fileData))

            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            fileData = dataSizeStr + fileData

            numSent = 0

            while len(fileData) > numSent:
                numSent += senderSocket.send(fileData[numSent:])

        else:
            break
    print(f"Server has sent {numSent} bytes")

    senderSocket.close()
    print("Sender data socket has been closed\n")
    fileObj.close()


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
            # Receive command from client
            command = connection_socket.recv(1024).decode()
            if debug == True:
                print("command received:", end='')
                print(command)
            
            # Server sends acknowledgement
            ack = f"Server recieved: {command}"
            connection_socket.sendall(ack.encode('utf-8'))

            # Server handles LS command, sends directory contents to client
            if command == 'ls':
                # print('Raw Response from server:\n')
                files = getFileList()
                # print(dir_list)
                #print('Response sent to client')
                lsResponse = f"Directory list: \n {files}"
                connection_socket.sendall(lsResponse.encode('utf-8'))

            # Server handles Get command
            elif command.startswith('get'):
                fileName = parseFileName(command)

                if fileExists(fileName) == False:
                    getResponse = "Error: File not found"
                    connection_socket.sendall(getResponse.encode('utf-8'))

                # File exists, send ACK
                else:
                    getResponse = f"Get Response: FileName detected: {fileName}"
                    connection_socket.sendall(getResponse.encode('utf-8'))

                    # Establish data socket
                    dataSocket(fileName) 


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