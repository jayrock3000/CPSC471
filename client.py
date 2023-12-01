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
# Main Method

def main():
    # Variable for debugging program
    

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
    
        # Close socket
        client_socket.close()

        try:
            with open('server_response.txt', 'r') as f:
                response = f.read()
                print(f'\n{response}')
            f.close()
        except:
            pass
        
        if debug == True:
            print("client socket has closed")

    print("client has quit")

################################################################
# Run main when program starts

if __name__ == "__main__":
    main()

#END