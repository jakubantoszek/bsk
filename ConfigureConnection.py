import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from utils import *
from constants import *


class ReceiveDataThread(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self):
        while True:
            response = self.client_socket.recv(1024)

            if response:
                print('Receiver:', response.decode('utf-8'))

class ConfigureConnection:
    def __init__(self, user_type, user_directory, public_key):
        self.entry = None
        self.address = None
        self.window = Tk()
        self.window.title("Configure connection: " + user_type)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=BACKGROUND_COLOR_DARKER)
        self.user_type = user_type
        self.user_socket = None
        self.user_directory = user_directory
        self.public_key = public_key
        self.other_client_key = None
        self.socket = None

        self.configure_connection_frame()

    def configure_connection_frame(self):
        frame = tk.Frame(self.window, bg=BACKGROUND_COLOR, padx=20, pady=20)
        frame.pack(pady=20)

        title_label = tk.Label(frame, text="Configure connection", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1)
        title_label.pack(pady=10)

        address_frame = tk.Frame(frame, bg=BACKGROUND_COLOR, padx=10, pady=10)
        address_frame.pack(pady=20)

        address_label = tk.Label(address_frame, text="Address:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR, fg=TEXT_COLOR2)
        address_label.pack()

        self.entry = tk.Entry(address_frame, font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.entry.pack()

        connect_button = tk.Button(frame, text='Connect', command=self.connect, font=BUTTON_FONT, bg=BUTTON_COLOR1, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1)
        connect_button.pack()

    def connect(self):
        self.address = self.entry.get()
        self.window.destroy()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.address, 8080))

        client_socket.send(self.public_key)
        response_key = client_socket.recv(1024)

        print("Mój klucz: ", self.public_key)
        print("Jego klucz: ", response_key)

        self.other_client_key = response_key
        self.socket = client_socket