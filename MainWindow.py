import os
import pickle
import socket
import tkinter as tk

from tkinter import filedialog
from tkinter import *
from utils import encrypt_data, decrypt_data
from constants import *
from functools import partial

ALGORITHM_OPTIONS = ["ECB", "CBC"]


class MainWindow:
    def __init__(self, host, port, encryption_key, decryption_key, client_socket, user_dir):
        self.message_entry = None
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.file_label = None
        self.encryption_key = encryption_key
        self.decryption_key = decryption_key
        self.socket = client_socket
        self.user_dir = user_dir
        self.chosen_file = None

        self.host = host
        self.port = port
        self.window = Tk()

        self.window.title("Main Window: " + self.user_dir[-1])
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=BACKGROUND_COLOR_DARKER)
        self.window.option_add("*Font", LABEL_FONT)
        self.radio_buttons = []

        self.create_main_frame()

    def create_main_frame(self):
        main_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR, padx=20, pady=10)
        main_frame.pack(pady=20)

        title_label = tk.Label(main_frame, text="Main Window", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1,
                               pady=5)
        title_label.pack(pady=10)

        message_frame = tk.LabelFrame(main_frame, text="Send message", font=LABEL_FONT, bg=BACKGROUND_COLOR,
                                      fg=TEXT_COLOR1, padx=10, pady=5)
        message_frame.pack()

        self.message_label = tk.Label(message_frame, text="Message:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                                      fg=TEXT_COLOR2)
        self.message_label.pack()

        self.message_entry = tk.Entry(message_frame, font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.message_entry.pack()

        options = ALGORITHM_OPTIONS
        self.selected_algorithm = tk.StringVar(message_frame)
        self.selected_algorithm.set(options[0])

        radio_frame = tk.Frame(message_frame, bg=BACKGROUND_COLOR, padx=10, pady=5)
        radio_frame.pack()

        for option in options:
            algorithm_radio = tk.Radiobutton(radio_frame, text=option, variable=self.selected_algorithm, value=option,
                                             font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                                             activebackground=BACKGROUND_COLOR, command=self.update_radio_buttons)
            algorithm_radio.pack(anchor=W)
            self.radio_buttons.append(algorithm_radio)
        self.update_radio_buttons()

        send_button = tk.Button(message_frame, text="Send", command=partial(self.send, "Message"), font=BUTTON_FONT,
                                bg=BUTTON_COLOR1, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1)
        send_button.pack()

        message_frame.pack(padx=10, pady=10)

        file_frame = tk.LabelFrame(main_frame, text="Send file", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1,
                                   padx=10)

        upload_button = tk.Button(file_frame, text="Choose file", command=self.upload_file, font=BUTTON_FONT,
                                  bg=BUTTON_COLOR2, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR2)
        upload_button.pack()

        self.file_label = tk.Label(file_frame, text="No file selected", font=MINI_FONT_BOLD, bg=BACKGROUND_COLOR,
                                   fg=TEXT_COLOR1, wraplength=190)
        self.file_label.pack()

        send_button = tk.Button(file_frame, text="Send", command=partial(self.send, "File"), font=BUTTON_FONT, bg=BUTTON_COLOR1,
                                fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1)
        send_button.pack(pady=5)

        file_frame.pack(padx=10, fill="x")

    def update_radio_buttons(self):
        for button in self.radio_buttons:
            if button["text"] == self.selected_algorithm.get():
                button.configure(fg=TEXT_COLOR1)
            else:
                button.configure(fg=TEXT_COLOR2)

    def upload_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.chosen_file = path
            file_name = os.path.basename(path)
            self.file_label.configure(text=file_name)

    def send_file(self):
        if self.chosen_file is not None:
            with open(self.chosen_file, 'rb') as file:
                content = file.read()
                client_socket = self.socket

                self.encryption_key = self.encryption_key[:32]
                self.decryption_key = self.decryption_key[:32]
                file_name = os.path.basename(self.chosen_file)

                data = {
                    'Type': "File",
                    'Content': content,
                    'Param': file_name
                }
                bytes_data = pickle.dumps(data)

                encrypted_message = encrypt_data(bytes_data, self.encryption_key,
                                                    self.selected_algorithm.get(), None)
                client_socket.send(encrypted_message)

                response = client_socket.recv(2048)
                response_message = decrypt_data(response, self.decryption_key)

                received_data = pickle.loads(response_message)
                with open(os.path.join(self.user_dir, received_data['Param']), 'wb') as received_file:
                    received_file.write(received_data['Content'])

    def send(self, message_type):
        client_socket = self.socket
        self.encryption_key = self.encryption_key[:32]
        self.decryption_key = self.decryption_key[:32]

        if message_type == "Message":
            encrypted_message = encrypt_data(self.message_entry.get().encode(),
                                             self.encryption_key,
                                             self.selected_algorithm.get())

            data = {
                'Type': "Message",
                'Mode': self.selected_algorithm.get(),
                'Content': encrypted_message
            }
            bytes_data = pickle.dumps(data)
            client_socket.send(bytes_data)
        else:
            if self.chosen_file is not None:
                with open(self.chosen_file, 'rb') as file:
                    content = file.read()
                    encrypted_content = encrypt_data(content,
                                                     self.encryption_key,
                                                     self.selected_algorithm.get())
                    file_name = os.path.basename(self.chosen_file)

                    data = {
                        'Type': "File",
                        'Mode': self.selected_algorithm.get(),
                        'Content': encrypted_content,
                        'Filename': file_name
                    }
                    bytes_data = pickle.dumps(data)
                    client_socket.send(bytes_data)

        response = client_socket.recv(2048)
        response_data = pickle.loads(response)
        response_content = decrypt_data(response_data['Content'],
                                        self.decryption_key,
                                        response_data['Mode'])

        if response_data['Type'] == "Message":
            print("Message received: ", response_content.decode())

            if self.message_entry.get().lower() == "exit":
                self.window.destroy()
                exit(0)
        else:
            print("File received: " + response_data['Filename'])
            new_file_path = os.path.join(self.user_dir, response_data['Filename'])

            with open(new_file_path, 'wb') as received_file:
                received_file.write(response_content)

# host = '127.0.0.1'  # Adres IP serwera
# port = 8080  # Port serwera
# encryption_key = 'myencryptionkey'  # Klucz szyfrowania
#
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((host, port))
#
# app = MainWindow(host, port, encryption_key, client_socket)
# app.window.mainloop()
