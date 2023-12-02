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
    
    directory = 'server_storage'

    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
        files = '\n- ' + '\n- '.join(files) + '\n'

        return files
        
    else:
        return 'Directory not found'


################################################################
# Determine the name of the file being requested

def parseFileName(command):
    if debug == True:
        print("parseFileName() function activated")
    
    # Remove get/put from commmand
    if command.startswith('get'):
        fileName = command.removeprefix('get ')
    elif command.startswith('put'):
        fileName = command.removeprefix('put ')

    if debug == True:
        print("fileName: " + fileName)

    return fileName

################################################################
# Function for checking if requested file exists

def fileExists(fileName):
    if debug == True:
        print("fileExists() function activated")

    directory = 'server_storage'
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
    
    if fileName in files:
        return True
    
    return False


################################################################
# Send file to client (Data channel for GET)
def getData(fileName):
    if debug == True:
        print("getData() function activated")

    # Connect to server
    receiverName = 'localhost'
    receiverPort = 5222

    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((receiverName, receiverPort))

    filePath = os.path.join("server_storage", fileName)

    fileObj = open(filePath, "r")
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
                chunk = fileData[numSent:].encode()
                numSent += senderSocket.send(chunk)

        else:
            break
    print(f"Server has sent {numSent} bytes")

    senderSocket.close()
    print("Sender data socket has been closed\n")
    fileObj.close()

################################################################
# Receive file from server (Data channel for GET)

def recvAll(sock, numBytes):
    recvBuff = ""
    tmpBuff = ""

    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes)
        if not tmpBuff:
            break

        recvBuff += tmpBuff.decode('utf-8')

    return recvBuff


def putData():
    if debug == True:
        print("putData() function activated")

    receiverName = 'localhost'
    receiverPort = 5333
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.bind((receiverName, receiverPort))
    receiverSocket.listen(1)

    # Accept connection
    while True:
        print(f"Server ready to receive on port {receiverPort}")

        senderSock, addr = receiverSocket.accept()
        print(f"Accepted connection from sender: {addr}\n")

        fileData = ""
        fileSize = 0
        fileSizeBuff = ""
        fileSizeBuff = recvAll(senderSock, 10)

        fileSize = int(fileSizeBuff)
        print(f"File size is: {fileSize}\n")

        fileData = recvAll(senderSock, fileSize)

        print(f"File data is: {fileData}\n")

        receiverSocket.close()
        print("Receiver data socket has been closed\n")
        
        return fileData

################################################################
# Main Method

def main():

    # Set up socket
    server_port = 5111
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

            # Server handles LS command
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
                    getData(fileName)

            # Server handles Put command
            elif command.startswith('put'):
                fileData = putData()
                fileName = parseFileName(command)
                filePath = os.path.join("server_storage", fileName)
                with open(filePath, 'w') as file:
                    file.write(fileData)
                ack = "File data has been written to ..." + filePath
                print(ack)
                connection_socket.sendall(ack.encode('utf-8'))

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