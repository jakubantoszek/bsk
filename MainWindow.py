import socket
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from utils import encrypt_message


class MainWindow:
    def __init__(self, host, port, encryption_key, client_socket):
        self.message_entry = None
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.file_label = None
        self.encryption_key = encryption_key
        self.socket = client_socket

        self.host = host
        self.port = port
        self.window = Tk()

        self.window.title("BSK")
        self.window.geometry('350x350')

        self.create_message_frame()
        self.create_file_frame()

    def create_message_frame(self):
        message_frame = tk.LabelFrame(self.window, text="Send message")
        options = ["ECB", "CBC"]

        entry_label = tk.Label(message_frame, text="Message: ")
        entry_label.pack()

        self.message_entry = tk.Entry(message_frame)
        self.message_entry.pack()

        self.selected_algorithm = tk.StringVar(message_frame)
        self.selected_algorithm.set(options[0])

        self.algorithm_menu = tk.OptionMenu(message_frame, self.selected_algorithm, *options)
        self.algorithm_menu.pack()

        send_button = tk.Button(message_frame, text='Send', command=self.send_message)
        send_button.pack()

        message_frame.pack(padx=10, pady=10)

    def create_file_frame(self):
        message_frame = tk.LabelFrame(self.window, text="Send file")
        options = ["ECB", "CBC"]

        upload_button = tk.Button(message_frame, text='Upload', command=self.upload_file)
        upload_button.pack()

        self.file_label = tk.Label(message_frame, text="No file selected")
        self.file_label.pack()

        self.selected_algorithm = tk.StringVar(message_frame)
        self.selected_algorithm.set(options[0])

        self.algorithm_menu = tk.OptionMenu(message_frame, self.selected_algorithm, *options)
        self.algorithm_menu.pack()

        send_button = tk.Button(message_frame, text='Send', command=self.send_file)
        send_button.pack()

        message_frame.pack(padx=10, pady=10)

    def upload_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_label.configure(text=path)

    def send_file(self):
        pass

    def send_message(self):
        client_socket = self.socket
        try:
            encrypted_message = encrypt_message(self.message_entry.get(),
                                                self.encryption_key,
                                                self.selected_algorithm.get())
            client_socket.send(encrypted_message)
            response = client_socket.recv(1024).decode()
            print("Odpowiedź serwera:", response)

            # Jeśli wiadomość to 'exit', zakończ połączenie
            if self.message_entry.get().lower() == 'exit':
                self.window.destroy()
                exit(0)
        finally:
            client_socket.close()
            exit(0)

