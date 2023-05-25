import socket
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from utils import *


class ConfigureConnection:
    def __init__(self, user_type):
        self.entry = None
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.address = None
        self.window = Tk()
        self.window.title("Configure connection: " + user_type)
        self.window.geometry('350x200')
        self.user_type = user_type
        self.user_socket = None

        # self.message = tk.Label(self.window, text="Opis ale nie wiem co tu napisac")
        # self.message.pack()

        self.generate_key_frame()

    def generate_key_frame(self):
        frame = tk.LabelFrame(self.window, text="Configure connection")

        entry_label = tk.Label(frame, text="Address: ")
        entry_label.pack()

        self.entry = tk.Entry(frame)
        self.entry.pack()

        send_button = tk.Button(frame, text='Connect', command=self.connect)
        send_button.pack()

        frame.pack(padx=10, pady=10)

    def connect(self):
        self.address = self.entry.get()
        # TODO obsługa błędów jak nie adres zostanie podany

        user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_socket = user_socket

        if self.user_type == "server":
            self.window.destroy()
            user_socket.bind((self.address, 8080))
            user_socket.listen()

            client, client_address = user_socket.accept()
            recv_message(self.address, 8080, client)
        else:
            self.window.destroy()
            user_socket.bind((self.address, 8081))
            user_socket.connect((self.address, 8080))

        user_socket.close()
