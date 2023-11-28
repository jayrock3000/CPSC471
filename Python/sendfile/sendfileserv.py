import socket

class FileReceiverServer:
    def __init__(self, listen_port):
        self.listen_port = listen_port
        self.welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.welcome_sock.bind(('', self.listen_port))
        self.welcome_sock.listen(1)

    def recv_all(self, sock, num_bytes):
        recv_buff = ""
        while len(recv_buff) < num_bytes:
            tmp_buff = sock.recv(num_bytes)
            if not tmp_buff:
                break
            recv_buff += tmp_buff
        return recv_buff

    def start_server(self):
        while True:
            print("Waiting for connections...")
            client_sock, addr = self.welcome_sock.accept()
            print("Accepted connection from client:", addr)
            file_data = ""
            file_size = 0
            file_size_buff = self.recv_all(client_sock, 10)
            file_size = int(file_size_buff)
            print("The file size is", file_size)
            file_data = self.recv_all(client_sock, file_size)
            print("The file data is:")
            print(file_data)
            client_sock.close()

# Usage
if __name__ == '__main__':
	listen_port = 1234
	file_server = FileReceiverServer(listen_port)
	file_server.start_server()
