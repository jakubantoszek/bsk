import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class GenerateKey:
    def __init__(self, user_dir, local_key):
        self.user_dir = user_dir
        self.local_key = local_key
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.window = Tk()
        self.window.title("Generate key")
        self.window.geometry('300x225')

        self.generate_key_frame()

    def generate_key_frame(self):
        frame = tk.LabelFrame(self.window, text="Creating public and private key")
        options = ["RSA1024", "RSA2048"]

        message = tk.LabelFrame(self.window, text="Opis ale nie wiem co tu napisac")
        message.pack()

        self.selected_algorithm = tk.StringVar(frame)
        self.selected_algorithm.set(options[0])

        self.algorithm_menu = tk.OptionMenu(frame, self.selected_algorithm, *options)
        self.algorithm_menu.pack()

        send_button = tk.Button(frame, text='Generate key', command=self.generate_key)
        send_button.pack()

        frame.pack(padx=10, pady=10)

    def generate_key(self):
        if self.selected_algorithm.get() == "RSA1024":
            (public_key, private_key) = rsa.newkeys(1024)
        else:
            (public_key, private_key) = rsa.newkeys(2048)

        public_key = public_key.save_pkcs1('PEM')
        private_key = private_key.save_pkcs1('PEM')

        self.window.destroy()
        self.save_keys(public_key, private_key)

    def save_keys(self, public_key, private_key):
        public_key_file = os.path.join(self.user_dir, "public_key.txt")
        private_key_file = os.path.join(self.user_dir, "private_key.txt")

        if not os.path.exists(public_key_file):
            with open(public_key_file, 'wb') as pu_file:
                pu_file.write(public_key)
            with open(private_key_file, 'wb') as pr_file:
                pr_file.write(self.encrypt_private_key(private_key))

    def encrypt_private_key(self, key):
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES256(self.local_key[:32].encode()),
                        modes.CBC(iv), default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES256.block_size).padder()
        padded_private_key = padder.update(key) + padder.finalize()

        encrypted_private_key = encryptor.update(padded_private_key) + encryptor.finalize()

        return iv + encrypted_private_key
