import socket
import os

debug = True

class FileReceiverServer:
    def __init__(self, listen_port):
        self.listen_port = listen_port
        self.welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_sock.bind(('', self.listen_port))
        self.welcome_sock.listen(1)
        
    def recv_all(self, sock, num_bytes):
        recv_buff = b""
        while len(recv_buff) < num_bytes:
            tmp_buff = sock.recv(num_bytes - len(recv_buff))
            if not tmp_buff:
                break
            recv_buff += tmp_buff
        return recv_buff


    def start_server(self):
        while True:
            print("Waiting for connections...")
            client_sock, addr = self.welcome_sock.accept()
            print("Accepted connection from client:", addr)
            
            # Receive the filename length
            filename_length_data = self.recv_all(client_sock, 10)
            filename_length = int(filename_length_data.decode('utf-8'))

            # Receive the filename
            filename_data = self.recv_all(client_sock, filename_length)
            filename = filename_data.decode('utf-8')
            # print("Received file name:", filename)

            # Receive the file size
            file_size_data = self.recv_all(client_sock, 10)
            file_size = int(file_size_data.decode('utf-8'))
            # print("The file size is", file_size)

            # Receive the file data
            file_data = self.recv_all(client_sock, file_size)

            with open(f'server_storage/{filename}', 'w') as f:
                f.write(file_data.decode('utf-8'))
            f.close()

            # print(f"The file data is: {filename}")
            
            # get file location, keep it here for an easier debug
            file_location = os.path.abspath(__file__)
            directory = os.path.dirname(file_location)

            # print(f'Saved to: {directory}') 



            if debug:
                print("Received file name:", filename)
                print("The file size is", file_size)
                print(f"File's data: {filename}")
                print(f'Saved to: {directory}') 

                                #### ATTENTION ####
                                
            # for future Minh, or for anyone gonna update this
            # Ensure we have a means to retrieve the precise location of the 'server_storage' folder.
            # Otherwise, it will only work on this (my laptop),
            # and upon installation on a new computer, the link/path MAY not work.
            with open('Python\sendfile\server_response2.txt', 'w') as file:
                file.write(f"Received file name: {filename}\n")
                file.write(f"The file size is: {file_size}\n")
                file.write(f"File's data:\n{file_data.decode('utf-8')}")
            file.close()

            client_sock.close()

# Usage
if __name__ == '__main__':
	listen_port = 1234
	file_server = FileReceiverServer(listen_port)
	print(f'Server is listening to port {listen_port}.')
	file_server.start_server()
