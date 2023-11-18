import socket
import os
import sys

class FileSenderClient:
    def __init__(self, server_address, server_port, file_name):
        self.server_address = server_address
        self.server_port = server_port
        self.file_name = file_name

    def send_file(self):
        # Open the file
        try:
            file_obj = open(self.file_name, "r")
        except FileNotFoundError:
            print("File not found.")
            return

        # Create a TCP socket
        conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        conn_sock.connect((self.server_address, self.server_port))

        num_sent = 0
        file_data = None

        while True:
            # Read 65536 bytes of data
            file_data = file_obj.read(65536)

            if file_data:
                # Get the size of the data read and convert it to string
                data_size_str = str(len(file_data))

                # Prepend 0's to the size string until the size is 10 bytes
                while len(data_size_str) < 10:
                    data_size_str = "0" + data_size_str

                # Prepend the size of the data to the file data
                file_data = data_size_str + file_data

                # The number of bytes sent
                num_sent = 0

                # Send the data
                while len(file_data) > num_sent:
                    num_sent += conn_sock.send(file_data[num_sent:])

            else:
                break

        print("Sent", num_sent, "bytes.")

        # Close the socket and the file
        conn_sock.close()
        file_obj.close()


if __name__ == '__main__':
	# Command line checks
	if len(sys.argv) < 2:
		print("USAGE python " + sys.argv[0] + " <FILE NAME>")
	else:
		# Server address
		serverAddr = "localhost"

		# Server port
		serverPort = 1234

		# The name of the file
		fileName = sys.argv[1]

		sender = FileSenderClient(serverAddr, serverPort, fileName)
		sender.send_file()
