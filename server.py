################################################################
# Group project for CPSC 471
# By Jeffrey Rhoten, Lucas Nguyen and Gia Minh Hoang
#
# Server.py
#
# IMPORTANT
# Please ensure any files you wish to transfer are
# located in the client_storage or server_storage
# folders in the same directory as client.py and
#
# Files must be .txt and less than MAX_FILE_SIZE
#
################################################################

# Import statements
import socket
import os

# Debug mode provides additional console messages
debug = False

# Global Variables
MAX_FILE_SIZE = 65536


################################################################
# Information header printed when program first runs

def programHeader():
    print("##################################################")
    print("Group project for CPSC 471")
    print("By Jeffrey Rhoten, Lucas Nguyen and Gia Minh Hoang\n")
    print("server.py\n")
    print("IMPORTANT")
    print("Please ensure any files you wish to transfer are")
    print("located in the client_storage or server_storage")
    print("folders in the same directory as client.py and server.py\n")
    print(f"Files must be .txt and less than {MAX_FILE_SIZE} bytes")
    print("##################################################\n")


################################################################
# Receive file from client (Server-side data channel for PUT command)

# Function called in putData, handles receipt of data from socket
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
def putData():
    if debug == True:
        print("putData() function activated")

    # Data link details
    receiverName = 'localhost'
    receiverPort = 5333
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.bind((receiverName, receiverPort))
    receiverSocket.listen(1)

    # Accept connection
    while True:
        print(f"Server ready to receive on port {receiverPort}")
        senderSock, addr = receiverSocket.accept()
        print(f"Accepted connection from sender: {addr}")
        fileData = ""
        fileSize = 0
        fileSizeBuff = ""
        fileSizeBuff = recvAll(senderSock, 10)

        # Establish buffer size
        fileSize = int(fileSizeBuff)
        print(f"File size is: {fileSize}")

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
# Send file to client (Server-side data channel for GET command)

def getData(fileName):
    if debug == True:
        print("getData() function activated")

    # Connect to server
    receiverName = 'localhost'
    receiverPort = 5222
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((receiverName, receiverPort))

    # File to be sent
    filePath = os.path.join("server_storage", fileName)
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
    print(f"Server has sent {numSent} bytes")

    # Close socket and file object
    senderSocket.close()
    if debug == True:
        print("Sender data socket has been closed\n")
    fileObj.close()


################################################################
# Function for ls command, returns list of all files on server (server_storage folder)

def getFileList():
    if debug == True:
        print("getFileList() function activated")
    
    # server_storage should be a folder located in the same directory as server.py
    directory = 'server_storage'

    # Check directory exists
    if os.path.exists(directory) and os.path.isdir(directory):

        # Retrieve list of files in directory
        files = os.listdir(directory)
        files = '\n- ' + '\n- '.join(files) + '\n'

        # Return list of files
        return files

    # Or return error message if directory not found
    else:
        return 'Directory not found'


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
    directory = 'server_storage'
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

    # Prepare socket, listen for clients
    server_port = 5111
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', server_port))
    server_socket.listen(1)
    print(f"FTP Server is ready on port {server_port}")


    # Prepare server to establish control channel
    while True:
        print("Waiting for connection...")
        
        # Establish control channel
        connection_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}.")
        

        # Control channel has been established


        # Process client commands
        while True:

            # Receive command from client
            command = connection_socket.recv(1024).decode()
            print(f"command received: {command}")
            
            # Server acknowledges command received
            ack = f"received command {command}"
            connection_socket.sendall(ack.encode('utf-8'))


            # Handle LS
            if command == 'ls':

                # Retrieve list of files in directory
                files = getFileList()

                # Prepare to deliver list to client
                lsResponse = f"Directory list: \n {files}"

                # Send to client
                connection_socket.sendall(lsResponse.encode('utf-8'))


            # Handle GET
            elif command.startswith('get'):

                # Determine name of file
                fileName = parseFileName(command)

                # Check file exists
                if fileExists(fileName) == False:

                    # Send error if can't find...
                    getResponse = "Error: File not found"
                    connection_socket.sendall(getResponse.encode('utf-8'))

                # ...or send confirmation file was found...
                else:
                    getResponse = f"Get Response: FileName detected: {fileName}"
                    connection_socket.sendall(getResponse.encode('utf-8'))

                    # ... and call function to send file
                    getData(fileName)


            # Handle PUT
            elif command.startswith('put'):

                # Call function to receive file data
                fileData = putData()

                # Determine where to save data
                fileName = parseFileName(command)
                filePath = os.path.join("server_storage", fileName)

                # Save file data to disk
                try:
                    with open(filePath, 'w') as file:
                        file.write(fileData)

                    # Print/Send confirmation ACK
                    ack = "File data has been written to ..." + filePath
                    print(ack)
                    connection_socket.sendall(ack.encode('utf-8'))

                # Catch exception for missing storage folder
                except:
                    nak = "server_storage folder missing\nfile transfer failed"
                    print(nak)
                    connection_socket.sendall(nak.encode('utf-8'))
                

            # Handle QUIT (server closes)
            elif command == 'quit':
                connection_socket.close()
                print("server socket has closed")
                print("server has quit")
                exit()


            # Close socket
            connection_socket.close()
            print("server socket has closed")
            break


################################################################
# Run main when program starts

if __name__ == "__main__":
    main()

#END of server.py