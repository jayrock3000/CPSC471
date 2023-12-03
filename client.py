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
# Information header printed when program first runs

def programHeader():
    if debug == True:
        print("programHeader() activated")

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
# Input verification to ensure only ls, get-, put-, and quit commands returned

def commandInput():
    if debug == True:
        print("commandInput() function activated")

    userInput = ""
    validInputs = ['ls', 'quit'] #Get and Put handled separately
    emptyName = ['get', 'get ', 'put', 'put '] #Handles empty get/put

    # Loop to repeatedly get inputs until valid one recognized
    while True:
        
        # Prompt ftp> shown each loop
        print('ftp> ', end='')
        
        userInput = input()
        try:
            userInput = str(userInput)

        # Error if user input causes exception / cannot be converted to string
        except:
            print("An error occurred with that input. Please try again.\n")
            continue

        # Catch blank inputs
        if userInput == "":
            print("Entry cannot be blank\n")
            continue

        # Catch empty get/put
        elif userInput in emptyName:
            print("get and put require a filename. Please try again\n")
            continue

        # Pass valid inputs
        elif userInput.startswith('get '):
            return userInput

        elif userInput.startswith('put '):
            return userInput

        elif userInput in validInputs:
            return userInput

        # Error if input detected but didn't match a valid input
        else:
            print("Invalid command. Please try again.\n")
            continue
        break


################################################################
# Send file to server (Client-side data channel for PUT command)

def putData(fileName):
    if debug == True:
        print("putData() function activated")

    # Connect to server
    receiverName = 'localhost'
    receiverPort = 5333
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((receiverName, receiverPort))

    # File to be sent
    filePath = os.path.join("client_storage", fileName)
    fileObj = open(filePath, "r")
    numSent = 0
    fileData = None

    # Loop until all data is sent
    while True:
        
        # Read file data
        fileData = fileObj.read(MAX_FILE_SIZE) #Max file size specified by global var

        if fileData:
            
            # Create data header
            dataSizeStr = str(len(fileData))

            # Append zeroes until 10 characters long
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            # Add header to file data
            fileData = dataSizeStr + fileData

            # Send data
            numSent = 0
            while len(fileData) > numSent:
                chunk = fileData[numSent:].encode()
                numSent += senderSocket.send(chunk)

        else:
            break

    # Print amount of data sent to console
    print(f"Client has sent {numSent} bytes")

    # Close socket and file object
    senderSocket.close()
    if debug == True:
        print("Sender data socket has been closed\n")
    fileObj.close()


################################################################
# Receive file from server (Client-side data channel for GET command)

# Function called in getData, handles receipt of data from socket
def recvAll(sock, numBytes):
    if debug == True:
        print("recvAll() function activated")
        
    recvBuff = ""
    tmpBuff = ""

    # Loop to repeatedly pull data from buffer
    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes)
        if not tmpBuff:
            break

        recvBuff += tmpBuff.decode('utf-8')

    # Return data once buffer empty
    return recvBuff

# Function for establishing data link
def getData():
    if debug == True:
        print("getData() function activated")
    
    # Data link details
    receiverName = 'localhost'
    receiverPort = 5222
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.bind((receiverName, receiverPort))
    receiverSocket.listen(1)

    # Accept connection
    while True:
        print(f"Client ready to receive on port {receiverPort}")

        senderSock, addr = receiverSocket.accept()
        print(f"Accepted connection from sender: {addr}")

        fileData = ""
        fileSize = 0
        fileSizeBuff = ""
        fileSizeBuff = recvAll(senderSock, 10)

        # Establish buffer size
        fileSize = int(fileSizeBuff)
        print(f"File size is: {fileSize}\n")

        # Receive data (invoking recvAll function)
        fileData = recvAll(senderSock, fileSize)

        # Print file data to console
        #print(f"File data is: {fileData}\n")

        # Close socket
        receiverSocket.close()
        if debug == True:
            print("Receiver data socket has been closed\n")
        
        # Return data (write to disk occurs later)
        return fileData
 

################################################################
# Simple function to determine name of file in given command

def parseFileName(command):
    if debug == True:
        print("parseFileName() function activated")
    
    # Remove get/put from commmand
    if command.startswith('get'):
        fileName = command.removeprefix('get ')
    elif command.startswith('put'):
        fileName = command.removeprefix('put ')

    # Return the pure filename
    return fileName


################################################################
# Function for checking if file exists in the appropriate directory

def fileExists(fileName):
    if debug == True:
        print("fileExists() function activated")

    # Directory that will be checked for file
    directory = 'client_storage' 
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)
    
    # Look for file in the directory
    while(True):
        try:
            if fileName in files:
                return True
            
            # Catch nonexistant file
            else:
                return False
        
        # Catch nonexistant directory
        except:
            return False
    
    # Backup catch nonexistant file
    return False


################################################################
# Main Method

def main():
    if debug == True:
        print("main() activated")

    # Print header to provide program info
    programHeader()


    # Prepare for server connection
    server_name = 'localhost'
    server_port = 5111
    while(True):

        # Attempt to connect to server
        try:
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_name, server_port))
            print(f"\nConnected to server on port {server_port}")
            break

        # Try again if server not found
        except:
            print(f"Server not found on port {server_port}, trying again in 5 seconds")
            time.sleep(5)
    

    # Control channel has been established


    # Notify user which commands are valid
    print("Valid commands: ls, get, put, quit\n")

    # Prepare to get commands from user
    command = ''
    while command != 'quit':        # Quit closes both user & server
  
        # Get command from user & validate
        command = commandInput()


        # Initial handling of PUT, check file exists
        if command.startswith('put'):

            # Determine the file name
            fileName = parseFileName(command)
            filePath = os.path.join("client_storage", fileName)

            # Check directory for file
            if fileExists(fileName) == False:
                print(f"Sorry, the file {filePath} could not be found, please try again\n")
                continue
                # File not found, get new command from client


        # Establish socket for command
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_name, server_port))

        if debug == True:
            print("sending command")

        # Send command to server
        client_socket.send(command.encode())

        # Client receives acknowledgement server received command
        ack = client_socket.recv(1024)
        print(f"Server response: {ack.decode('utf-8')}")


        # Handle PUT
        if command.startswith('put'):

            # Establish data link & send file
            putData(fileName)

            # Wait for server to ACK file received
            ack = client_socket.recv(1024)
            print(f"\nServer response: {ack.decode('utf-8')}\n")


        # Handle LS
        elif command == 'ls':

            # Receive response from server
            lsResponse = client_socket.recv(1024)

            # Print results
            print(f"\n{lsResponse.decode('utf-8')}")


        # Handle GET
        elif command.startswith('get'):

            # Receive ACK from server (whether file exists)
            getResponse = client_socket.recv(1024)

            # If file doesn't exist, print error msg
            if getResponse.decode('utf-8') == "Error: File not found":
                print("Server response:\n    Error: File not found\n")
                client_socket.close()
                continue

            # Else file exists, so receive file
            else:
                # Print confirmation
                print(f"{getResponse.decode('utf-8')}")

                # Call function to receive file data
                fileData = getData()

                # Determine where to save data
                fileName = parseFileName(command)
                filePath = os.path.join("client_storage", fileName)

                # Save file data to disk
                with open(filePath, 'w') as file:
                    file.write(fileData)

                # Print confirmation
                print(f"File data has been written to .../{filePath}\n")


        # Close socket
        client_socket.close()
        if debug == True:
            print("client socket has closed")

    # Quit message to indicate program closes successfully
    print("client has quit")


################################################################
# Run main when program starts

if __name__ == "__main__":
    main()

#END of client.py