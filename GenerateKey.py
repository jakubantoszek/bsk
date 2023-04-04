import tkinter as tk
from tkinter import filedialog
from tkinter import *


class GenerateKey:
    def __init__(self):
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.window = Tk()
        self.window.title("Generate key")
        self.window.geometry('300x225')

        self.generate_key_frame()

    def generate_key_frame(self):
        frame = tk.LabelFrame(self.window, text="Creating public key")
        options = ["RSA1024", "RSA2048"]

        message = tk.LabelFrame(frame, text="Opis ale nie wiem co tu napisac")
        message.pack()
        
        self.selected_algorithm = tk.StringVar(frame)
        self.selected_algorithm.set(options[0])

        self.algorithm_menu = tk.OptionMenu(frame, self.selected_algorithm, *options)
        self.algorithm_menu.pack()

        send_button = tk.Button(frame, text='Generate key', command=self.generate_key)
        send_button.pack()

        frame.pack(padx=10, pady=10)

    def generate_key(self):
        self.window.destroy()
