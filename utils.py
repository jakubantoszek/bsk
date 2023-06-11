import os.path
import secrets
import socket

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_pad


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

    print(type(public_key))

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


def encrypt_session_key(encoding_key, session_key):
    encrypted_session_key = encoding_key.encrypt(
        session_key,
        asymmetric_pad.OAEP(
            mgf=asymmetric_pad.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_session_key


def get_session_key(encoding_key):
    session_key = os.urandom(32)
    return encrypt_session_key(encoding_key, session_key)


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
        padder = padding.PKCS7(128).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()

        encryption_key = encryption_key[:32]

        # Create an AES cipher object with ECB mode
        cipher = Cipher(algorithms.AES(encryption_key), modes.ECB(), backend=default_backend())

        # Create an encryptor object
        encryptor = cipher.encryptor()

        # Encrypt the padded message
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

        # Return the encrypted message as bytes
        return encrypted_message
    elif mode == 'CBC':
        iv = os.urandom(16)
        block_size = algorithms.AES.block_size // 8

        padded_message = pad_message(message, block_size, 'CBC')

        cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv),
                        backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        return ciphertext


def public_key_to_bytes(public_key):
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_bytes


def bytes_to_public_key(public_key_bytes):
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )
    return public_key
