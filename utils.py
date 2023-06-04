import os.path
import secrets
import socket

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


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


def encrypt_session_key(session_key, encoding_key):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES256(encoding_key[:32]),
                    modes.CBC(iv), default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES256.block_size).padder()
    padded_private_key = padder.update(session_key) + padder.finalize()
    encrypted_private_key = encryptor.update(padded_private_key) + encryptor.finalize()

    return iv + encrypted_private_key


def get_session_key(encoding_key):
    session_key = secrets.token_bytes(16)
    return encrypt_session_key(session_key, encoding_key)


def pad_message(message, block_size, mode):
    if mode == 'ECB':
        # Calculate the number of padding bytes required
        padding_length = block_size - (len(message) % block_size)

        # Pad the message with the required number of bytes
        padded_message = message + padding_length * bytes([padding_length])

        return padded_message
    elif mode == 'CBC':
        padding_length = block_size - (len(message) % block_size)
        padded_message = message + bytes([padding_length]) * padding_length
        return padded_message


def encrypt_message(message, encryption_key, mode):
    if mode == 'ECB':
        block_size = algorithms.AES.block_size // 8

        # Pad the message to a multiple of the block size
        padded_message = pad_message(message, block_size, 'ECB')

        # Create an AES cipher with ECB mode
        cipher = Cipher(algorithms.AES(encryption_key), modes.ECB(),
                        backend=default_backend())

        # Create an encryptor object
        encryptor = cipher.encryptor()

        # Encrypt the padded message
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()

        return ciphertext
    elif mode == 'CBC':
        iv = os.urandom(16)
        block_size = algorithms.AES.block_size // 8

        padded_message = pad_message(message, block_size, 'CBC')

        cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv),
                        backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        return ciphertext
