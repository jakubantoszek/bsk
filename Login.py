import tkinter as tk


class Login:
    def __init__(self):
        self.repeat_password_entry = None
        self.repeat_password_label = None
        self.register_button = None
        self.password_entry = None
        self.login_button = None
        self.username_entry = None
        self.password_label = None
        self.username_label = None

        self.create_window('Login')
        self.window.mainloop()

    def create_window(self, window_type):
        self.window = tk.Tk()
        self.window.geometry('600x450')

        if window_type == 'Login':
            self.window.title("Login")
            self.login_window()
        elif window_type == 'Register':
            self.window.title("Register")
            self.register_window()

    def login_window(self):
        self.username_label = tk.Label(self.window, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.window, text="Login", command=lambda: self.login('Login'))
        self.login_button.pack()

        self.register_button = tk.Button(self.window, text="Register", command=lambda: self.register('Login'))
        self.register_button.pack()

    def register_window(self):
        self.username_label = tk.Label(self.window, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        self.repeat_password_label = tk.Label(self.window, text="Repeat password:")
        self.repeat_password_label.pack()

        self.repeat_password_entry = tk.Entry(self.window, show="*")
        self.repeat_password_entry.pack()

        self.register_button = tk.Button(self.window, text="Register", command=lambda: self.register('Register'))
        self.register_button.pack()

        self.login_button = tk.Button(self.window, text="Login", command=lambda: self.login('Register'))
        self.login_button.pack()

    def login(self, window_type):
        if window_type == 'Login':
            print("Login")
            self.window.destroy()
        elif window_type == 'Register':
            self.window.destroy()
            self.create_window('Login')

    def register(self, window_type):
        if window_type == 'Register':
            print("Register")
            self.window.destroy()
        elif window_type == 'Login':
            self.window.destroy()
            self.create_window('Register')
