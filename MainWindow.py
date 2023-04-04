import tkinter as tk
from tkinter import filedialog
from tkinter import *


class MainWindow:
    def __init__(self):
        self.file_label = None
        self.window = Tk()

        self.window.title("BSK")
        self.window.geometry('640x480')

        self.create_widgets()

    def create_widgets(self):
        upload_button = tk.Button(self.window, text='Upload', command=self.upload_file)
        upload_button.pack()

        self.file_label = tk.Label(self.window, text="No file selected")
        self.file_label.pack()

    def upload_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_label.configure(text=path)
