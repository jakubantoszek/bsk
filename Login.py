import tkinter as tk


class Login:
    def __init__(self):
        self.register_button = None
        self.password_entry = None
        self.login_button = None
        self.username_entry = None
        self.password_label = None
        self.username_label = None
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry('600x450')

        self.login_window()

    def login_window(self):
        self.username_label = tk.Label(self.window, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.window, text="Register", command=self.register)
        self.register_button.pack()

    def login(self):
        print("Login")
        self.window.destroy()

    def register(self):
        print("Register")
        self.window.destroy()
