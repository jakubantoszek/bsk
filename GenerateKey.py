import os
import tkinter as tk
from tkinter import *

import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from constants import *
from utils import get_key_from_file


class GenerateKey:
    def __init__(self, user_dir, local_key):
        self.user_dir = user_dir
        self.local_key = local_key
        self.selected_algorithm = None
        self.window = Tk()
        self.window.title("Generate key")
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=BACKGROUND_COLOR_DARKER)
        self.public_key = None
        self.radio_buttons = []

        self.generate_key_frame()

    def generate_key_frame(self):
        frame = tk.Frame(self.window, bg=BACKGROUND_COLOR, padx=20, pady=20)
        frame.pack(pady=20)

        title_label = tk.Label(frame, text="Keys", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1)
        title_label.pack(pady=10)

        message = tk.Label(frame, text="Creating public and private key", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                           fg=TEXT_COLOR2)
        message.pack(pady=10)

        options = ["RSA1024", "RSA2048"]
        self.selected_algorithm = tk.StringVar(frame)
        self.selected_algorithm.set(options[0])

        radio_frame = tk.Frame(frame, bg=BACKGROUND_COLOR, padx=10, pady=10)
        radio_frame.pack(pady=20)

        for option in options:
            algorithm_button = tk.Radiobutton(radio_frame, text=option, variable=self.selected_algorithm, value=option,
                                              font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                                              activebackground=BACKGROUND_COLOR, command=self.update_radio_buttons)
            algorithm_button.pack(anchor=W)
            self.radio_buttons.append(algorithm_button)

        self.update_radio_buttons()

        send_button = tk.Button(frame, text='Generate key', command=self.generate_key, font=BUTTON_FONT,
                                bg=BUTTON_COLOR1, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1)
        send_button.pack()

    def update_radio_buttons(self):
        for button in self.radio_buttons:
            if button["text"] == self.selected_algorithm.get():
                button.configure(fg=TEXT_COLOR1)
            else:
                button.configure(fg=TEXT_COLOR2)

    def generate_key(self):
        self.window.destroy()
        try:
            self.public_key = get_key_from_file(self.user_dir)
        except FileNotFoundError:
            if self.selected_algorithm.get() == "RSA1024":
                (public_key, private_key) = rsa.newkeys(1024)
            else:
                (public_key, private_key) = rsa.newkeys(2048)

            public_key = public_key.save_pkcs1('PEM')
            private_key = private_key.save_pkcs1('PEM')

            self.public_key = public_key
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

        cipher = Cipher(algorithms.AES256(self.local_key[:32].encode()), modes.CBC(iv), default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES256.block_size).padder()
        padded_private_key = padder.update(key) + padder.finalize()

        encrypted_private_key = encryptor.update(padded_private_key) + encryptor.finalize()

        return iv + encrypted_private_key
