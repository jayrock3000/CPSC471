import socket

# Variable for debugging program
debug = True

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


# Connect to server
server_name = 'localhost'
server_port = 5432


# Send commands to the server
#command = input("Enter command (ls, get, put, quit): ")

command = ''
while command != 'quit':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    command = commandInput()
    client_socket.send(command.encode())
    client_socket.close()
    if debug == True:
        print("client socket has closed")

# Handle server responses and file transfers
# Your implementation for handling server responses and file transfers goes here

print("client has quit")