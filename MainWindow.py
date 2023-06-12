import os
import pickle
import tkinter as tk
import socket

from tkinter import filedialog
from tkinter import *
from utils import encrypt_data, decrypt_data
from constants import *
from functools import partial

ALGORITHM_OPTIONS = ["ECB", "CBC"]


class MainWindow:
    def __init__(self, encryption_key, decryption_key, client_socket, user_dir):
        # window settings
        self.window = Tk()
        self.window.title("Main Window: " + user_dir[-1])
        self.window.geometry(WINDOW_DOUBLE_SIZE)
        self.window.configure(bg=BACKGROUND_COLOR_DARKER)
        self.window.option_add("*Font", LABEL_FONT)

        # entries and buttons
        self.radio_buttons = []
        self.file_label = None
        self.message_entry = None
        self.selected_algorithm = None
        self.chosen_file = None

        # other variables
        self.encryption_key = encryption_key[:32]
        self.decryption_key = decryption_key[:32]
        self.socket = client_socket
        self.user_dir = user_dir

        self.create_main_frame()

    def create_main_frame(self):
        main_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR, padx=20, pady=10)
        main_frame.pack(pady=20, expand=True)

        title_label = tk.Label(main_frame, text="Main Window", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1)
        title_label.pack()

        # Left Frame - Message and File
        left_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        left_frame.pack(side="left", padx=10, pady=10)

        message_frame = tk.LabelFrame(left_frame, text="Send message", font=LABEL_FONT, bg=BACKGROUND_COLOR,
                                      fg=TEXT_COLOR1, padx=10, pady=5)
        message_frame.pack()

        self.message_label = tk.Label(message_frame, text="Message:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                                      fg=TEXT_COLOR2)
        self.message_label.pack()

        self.message_entry = tk.Entry(message_frame, font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.message_entry.pack()

        send_button = tk.Button(message_frame, text="Send", command=partial(self.send, "Message"), font=BUTTON_FONT,
                                bg=BUTTON_COLOR1, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1)
        send_button.pack(pady=5)

        message_frame.pack(padx=10, pady=10)

        file_frame = tk.LabelFrame(left_frame, text="Send file", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1,
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


        options = ALGORITHM_OPTIONS
        self.selected_algorithm = tk.StringVar(left_frame)
        self.selected_algorithm.set(options[0])

        radio_frame = tk.Frame(left_frame, bg=BACKGROUND_COLOR, padx=10, pady=5)
        radio_frame.pack(anchor="center", pady=5)

        radio_label = tk.Label(radio_frame, text="Choose encryption mode:", font=LABEL_FONT, bg=BACKGROUND_COLOR,
                                      fg=TEXT_COLOR1)
        radio_label.pack()

        for option in options:
            algorithm_radio = tk.Radiobutton(radio_frame, text=option, variable=self.selected_algorithm, value=option,
                                             font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                                             activebackground=BACKGROUND_COLOR, command=self.update_radio_buttons)
            algorithm_radio.pack(anchor="center")
            self.radio_buttons.append(algorithm_radio)
        self.update_radio_buttons()


        # Right Frame - Received Messages
        right_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        right_frame.pack(side="right", padx=10, pady=10)

        received_messages_label = tk.Label(right_frame, text="Received messages:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR,
                                           fg=TEXT_COLOR2, pady=5)
        received_messages_label.pack(pady=10)

        self.received_messages_text = tk.Text(right_frame, font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR,
                                              height=32, width=20)
        self.received_messages_text.pack()

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

    def send(self, message_type):  # send file or message with additional parameters
        client_socket = self.socket

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
            received_message = "Message received: " + response_content.decode()
            print(received_message)
            self.received_messages_text.insert(tk.END, received_message + "\n")

            if self.message_entry.get().lower() == "exit":
                self.window.destroy()
                exit(0)
        else:
            received_file = "File received: " + response_data['Filename']
            print(received_file)
            self.received_messages_text.insert(tk.END, received_file + "\n")
            new_file_path = os.path.join(self.user_dir, response_data['Filename'])

            with open(new_file_path, 'wb') as received_file:
                received_file.write(response_content)
