# CPSC471
Group project for CPSC 471 at CSUF

# Names and email address:

Lucas Nguyen - LucasDNguyen@csu.fullerton.edu

Jeffrey Rhoten - jeffrhoten@csu.fullerton.edu

Gia Minh Hoang - minhhg16@csu.fullerton.edu


# TLDR Instructions

1. There should be folders called client_storage and server_storage in the same directory as client.py and server.py respectively
	- Ensure any files you wish to get or put via FTP are located in client_storage or server_storage

2. Run server.py
	- server.py will establish the control channel through a predetermined port

3. Run client.py
	- client.py will connect to the server and can send commands through the control channel

4. Enter commands into the terminal for client.py
	- Valid commands are [ls, get, put, quit]




# Simple FTP (File Transfer Protocol) Service

This repository contains a simple implementation of an FTP service using Python. The service comprises two main scripts: client.py and server.py. These scripts allow users to transfer files between a client and server using basic command functionalities such as 'ls', 'get', 'put', and 'quit'.


**Files:** 

1. client.py
	The client.py script is responsible for handling client-side operations for file transfer. Key functionalities include:
		- Listing Files (ls): Lists files available on the server.

		- Downloading Files (get): Downloads files from the server to the client's local storage.

		- Uploading Files (put): Uploads files from the client's local storage to the server.

		- Exiting the Client (quit): Closes the client application.

2. server.py
	The server.py script manages server-side operations for file transfer. It receives commands from the client through the control channel. Its functionality includes:
		- Listing Files (ls): Displays the list of files available on the server.

		- Downloading Files (get): Sends requested files from the server to the client.

		- Uploading Files (put): Receives files from the client and stores them on the server.

		- Quitting the Server (quit): Terminates the server application.

 **Server Setup:**

	Place files you wish to share in the server_storage directory.
	Run server.py to start the server.

**Client Setup:**

	Place files to be uploaded in the client_storage directory.
	Run client.py to connect to the server.
	Commands:
		- Use commands like ls, get [file_name], put [file_name], and quit to perform operations.

# Important Notes:
	Files must be in .txt format and smaller than MAX_FILE_SIZE bytes for transfer.
	Ensure the client and server scripts are in the same directory as their respective storage folders.
	Ensure Python 3.x is installed on your system. 
	(This program was built using **Python 3.10.5**)
