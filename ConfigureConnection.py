import tkinter as tk
from tkinter import filedialog
from tkinter import *


class ConfigureConnection:
    def __init__(self):
        self.entry = None
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.window = Tk()
        self.window.title("Configure connection")
        self.window.geometry('300x200')

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
        self.window.destroy()
