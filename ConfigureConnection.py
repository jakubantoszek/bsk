import tkinter as tk
from tkinter import *
import socket

from constants import *
from utils import *


class ConfigureConnection:
    def __init__(self, public_key):
        # window-related variables
        self.entry = None
        self.window = Tk()
        self.window.title("Configure connection")
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=BACKGROUND_COLOR_DARKER)

        # other variables
        self.address = None
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

        address_label = tk.Label(address_frame, text="Address:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                                 fg=TEXT_COLOR2)
        address_label.pack()

        self.entry = tk.Entry(address_frame, font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.entry.pack()

        connect_button = tk.Button(frame, text='Connect', command=self.connect, font=BUTTON_FONT, bg=BUTTON_COLOR1,
                                   fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1)
        connect_button.pack()

    def connect(self):
        self.address = self.entry.get()

        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.address, 8080))

        # Keys exchange
        client_socket.send(public_key_to_bytes(self.public_key))
        response_key = client_socket.recv(2048)

        self.other_client_key = bytes_to_public_key(response_key)
        self.socket = client_socket

        self.window.destroy()
