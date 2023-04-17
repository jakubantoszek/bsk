import tkinter as tk
from tkinter import filedialog
from tkinter import *
import rsa


class GenerateKey:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.algorithm_menu = None
        self.selected_algorithm = None
        self.window = Tk()
        self.window.title("Generate key")
        self.window.geometry('300x225')

        self.generate_key_frame()

    def generate_key_frame(self):
        frame = tk.LabelFrame(self.window, text="Creating public and private key")
        options = ["RSA1024", "RSA2048"]

        message = tk.LabelFrame(self.window, text="Opis ale nie wiem co tu napisac")
        message.pack()
        
        self.selected_algorithm = tk.StringVar(frame)
        self.selected_algorithm.set(options[0])

        self.algorithm_menu = tk.OptionMenu(frame, self.selected_algorithm, *options)
        self.algorithm_menu.pack()

        send_button = tk.Button(frame, text='Generate key', command=self.generate_key)
        send_button.pack()

        frame.pack(padx=10, pady=10)

    def generate_key(self):
        if self.selected_algorithm.get() == "RSA1024":
            (public_key, private_key) = rsa.newkeys(1024)
        else:
            (public_key, private_key) = rsa.newkeys(2048)

        self.public_key = public_key.save_pkcs1('PEM')
        self.private_key = private_key.save_pkcs1('PEM')
        self.window.destroy()
