import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []

    def handle_client(self, client_socket):
        # handle incoming messages from a client
        while True:
            data = client_socket.recv(2048)
            if not data:
                break
            self.broadcast(data, client_socket)  # send message to other client

        client_socket.close()
        self.clients.remove(client_socket)

    def broadcast(self, data, sender_socket):
        # Send a data to all connected clients
        for client_socket in self.clients:
            if client_socket != sender_socket:
                client_socket.send(data)

    def exchange_keys(self):
        client_sockets = self.clients

        key = client_sockets[0].recv(2048)
        client_sockets[1].send(key)

        key = client_sockets[1].recv(2048)
        client_sockets[0].send(key)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(2)

        print("The server is listening on {}:{}".format(self.host, self.port))

        while len(self.clients) < 2:
            client_socket, addr = server_socket.accept()
            print('Connected to:', addr)
            self.clients.append(client_socket)

        self.exchange_keys()

        for client_socket in self.clients:
            # start new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

        server_socket.close()


server = Server('127.0.0.1', 8080)
server.start_server()
