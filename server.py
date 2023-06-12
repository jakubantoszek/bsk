import socket


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("The server is listening on {}:{}".format(host, port))

    client_sockets = []
    while len(client_sockets) < 2:  # waiting for both users
        connection, address = server_socket.accept()
        client_sockets.append(connection)
        print("Connected with: ", address)

    while True:
        message = client_sockets[0].recv(2048)
        client_sockets[1].send(message)

        message = client_sockets[1].recv(2048)
        client_sockets[0].send(message)

    for client_socket in client_sockets:
        client_socket.close()

    server_socket.close()


start_server('127.0.0.1', 8080)
