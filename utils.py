import os.path
import socket

from cryptography.hazmat.primitives import serialization


def recv_message(host, port, conn):
    try:
        data = conn.recv(1024)
        message = data.decode()
        print(message)
    finally:
        conn.close()


def get_key_from_file(directory):
    with open(os.path.join(directory, 'public_key.txt'), 'rb') as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(), None
        )

    return public_key


def send_public_key(directory, user_socket):
    public_key = get_key_from_file(directory)
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    user_socket.sendall(serialized_public_key)


def receive_public_key(user_socket):
    serialized_pub_key = user_socket.recv(2048)
    public_key = serialization.load_pem_public_key(
        serialized_pub_key, None
    )

    return public_key
