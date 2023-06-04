import socket


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("Serwer nasłuchuje na {}:{}".format(host, port))

    client_sockets = []
    while len(client_sockets) < 2:
        connection, address = server_socket.accept()
        client_sockets.append(connection)
        print("Połączenie nawiązane z:", address)

    while True:
        message = client_sockets[0].recv(1024)
        client_sockets[1].send(message)

        message = client_sockets[1].recv(1024)
        client_sockets[0].send(message)

    for client_socket in client_sockets:
        client_socket.close()

    server_socket.close()


start_server('127.0.0.1', 8080)
