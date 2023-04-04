import tkinter as tk
from tkinter import filedialog
from tkinter import *


class MainWindow:
    def __init__(self):
        self.message_entry = None
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.file_label = None
        self.window = Tk()

        self.window.title("BSK")
        self.window.geometry('640x480')

        self.create_message_frame()
        self.create_file_frame()

    def create_message_frame(self):
        message_frame = tk.LabelFrame(self.window, text="Send message")
        options = ["ECB", "CBC"]

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
        pass
