################################################################
# Group project for CPSC 471
# By Jeffrey Rhoten, Lucas Nguyen and Gia Minh Hoang
#
# Client.py
#
# IMPORTANT
# Please ensure any files you wish to transfer are
# located in the client_storage or server_storage
# folders in the same directory as client.py and
#
# Files must be .txt and less than MAX_FILE_SIZE bytes
#
################################################################
# Import statements

import socket
import os
import time

# Debug mode provides additional console messages
debug = False

# Global Variables
MAX_FILE_SIZE = 65536

################################################################
# Print header for group project

def programHeader():
    print("##################################################")
    print("Group project for CPSC 471")
    print("By Jeffrey Rhoten, Lucas Nguyen and Gia Minh Hoang\n")
    print("client.py\n")
    print("IMPORTANT")
    print("Please ensure any files you wish to transfer are")
    print("located in the client_storage or server_storage")
    print("folders in the same directory as client.py and server.py\n")
    print(f"Files must be .txt and less than {MAX_FILE_SIZE} bytes")
    print("##################################################\n")

################################################################
# Function to get user input for commands
# Input verification to ensure only ls, get, put, and quit are returned

def commandInput():
    if debug == True:
        print("commandInput() function activated")

    userInput = ""

    print("Valid commands: ls, get, put, quit")

    while True:
        print('ftp> ', end='')
        validInputs = ['ls', 'quit']
        userInput = input()
        try:
            userInput = str(userInput)

        except:
            print("An error occurred with that input. Please try again.\n")
            continue

        if userInput == "":
            print("Entry cannot be blank\n")
            continue

        elif userInput.startswith('get'):
            return userInput

        elif userInput.startswith('put'):
            return userInput

        elif userInput in validInputs:
            return userInput

        else:
            print("Invalid command. Please try again.\n")
            continue
        break

################################################################
# Send file to server (Data channel for GET)
def putData(fileName):
    if debug == True:
        print("putData() function activated")

    # Connect to server
    receiverName = 'localhost'
    receiverPort = 5333

    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((receiverName, receiverPort))

    filePath = os.path.join("client_storage", fileName)

    fileObj = open(filePath, "r")
    numSent = 0
    fileData = None

    # Send until all data is sent
    while True:
        fileData = fileObj.read(MAX_FILE_SIZE)

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

    print(f"Client has sent {numSent} bytes")

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


def getData():
    if debug == True:
        print("getData() function activated")

    receiverName = 'localhost'
    receiverPort = 5222
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.bind((receiverName, receiverPort))
    receiverSocket.listen(1)

    # Accept connection
    while True:
        print(f"Client ready to receive on port {receiverPort}")

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

    directory = 'client_storage'
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
    
    #print(files)
    if fileName in files:
        return True
    
    return False


################################################################
# Main Method

def main():

    # Print header for information about this program
    programHeader()

    # Connect to server
    server_name = 'localhost'
    server_port = 5111
    while(True):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_name, server_port))
            print(f"Connected to server on port {server_port}")
            break
        except:
            print(f"Server not found on port {server_port}, trying again in 5 seconds")
            time.sleep(5)

    command = ''
    while command != 'quit':        # Repeatedly get user input until "quit" entered

        # Get command from user
        command = commandInput()

        # Handle Put command
        if command.startswith('put'):
            # Determine the file name
            fileName = parseFileName(command)
            filePath = os.path.join("client_storage", fileName)

            # Check file exists
            if fileExists(fileName) == False:
                print(f"\nSorry, the file {filePath} could not be found, please try again\n")
                continue # Get new command from client

        # Establish socket for command
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_name, server_port))

        if debug == True:
            print("sending command")

        # Send command to server
        client_socket.send(command.encode())

        # Client receives acknowledgement
        ack = client_socket.recv(1024)
        print(f"Server response: {ack.decode('utf-8')}")

        # Handle get
        if command.startswith('put'):
            putData(fileName)

            # Wait for server to ACK file received
            ack = client_socket.recv(1024)
            print(f"Server response: {ack.decode('utf-8')}")

        # Handle ls
        elif command == 'ls':
            lsResponse = client_socket.recv(1024)
            print(f"\n{lsResponse.decode('utf-8')}")

        # Handle get
        elif command.startswith('get'):
            getResponse = client_socket.recv(1024)

            if getResponse.decode('utf-8') == "Error: File not found":
                print("\nServer was not able to find the file\n")
                client_socket.close()
                continue

            else:
                print(f"\n{getResponse.decode('utf-8')}")
                fileData = getData()
                fileName = parseFileName(command)
                filePath = os.path.join("client_storage", fileName)
                with open(filePath, 'w') as file:
                    file.write(fileData)
                print(f"\nFile data has been written to .../{filePath}\n")




        # Close socket
        client_socket.close()

        """
        try:
            with open('server_response.txt', 'r') as f:
                response = f.read()
                print(f'\n{response}')
            f.close()
        except:
            pass
        """
        
        if debug == True:
            print("client socket has closed")

    print("client has quit")

################################################################
# Run main when program starts

if __name__ == "__main__":
    main()

#END