################################################################
# Group project for CPSC 471
# By Jeffrey Rhoten, Lucas Nguyen and Minh Gia Hoang
#
# Client.py
################################################################
# Import statements

import socket

# Debug mode provides additional console messages
debug = True

################################################################
# Function to get user input for commands
# Input verification to ensure only ls, get, put, and quit are returned

def commandInput():
    if debug == True:
        print("commandInput() function activated")

    userInput = ""

    while True:
        print("Enter command (ls, get, put, quit): ", end="")
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


def dataSocket():
    if debug == True:
        print("dataSocket() function activated")

    receiverName = 'localhost'
    receiverPort = 5433
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
        break


################################################################
# Main Method

def main():
    
    # Connect to server
    server_name = 'localhost'
    server_port = 5432


    command = ''
    while command != 'quit':        # Repeatedly get user input until "quit" entered

        # Get command from user
        command = commandInput()

        # Establish socket for command
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_name, server_port))
        if debug == True:
            print("sending command")

        # Send command to server
        client_socket.send(command.encode())

        # Client receives acknowledgement
        ack = client_socket.recv(1024)
        print(f"ACK from server: {ack.decode('utf-8')}")

        # Handle ls
        if command == 'ls':
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
                dataSocket()






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