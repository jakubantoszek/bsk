import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from utils import *


def receive_data(client_socket):
    while True:
        response = client_socket.recv(1024)

        if response:
            print('Receiver:', response.decode('utf-8'))


class ConfigureConnection:
    def __init__(self, user_type, user_directory, public_key):
        self.entry = None
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.address = None
        self.window = Tk()
        self.window.title("Configure connection: " + user_type)
        self.window.geometry('350x200')
        self.user_type = user_type
        self.user_socket = None
        self.user_directory = user_directory
        self.public_key = public_key

        # self.message = tk.Label(self.window, text="Opis ale nie wiem co tu napisac")
        # self.message.pack()

        if self.user_type == 'client':
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

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.address, 8080))

        client_socket.send(self.public_key)
        response_key = client_socket.recv(1024)

        print("Mój klucz: ", self.public_key)
        print("Jego klucz: ", response_key)

        client_socket.close()
