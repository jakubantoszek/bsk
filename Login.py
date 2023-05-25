import os.path
import tkinter as tk
import hashlib
path = "H:\\Studia\\Semestr 6\\bsk_users"


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
        self.user_directory = None

        self.create_window('Login')
        self.window.mainloop()

    def create_window(self, window_type):
        self.window = tk.Tk()
        self.window.geometry('250x250')

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
            user_dir = os.path.join(path, self.username_entry.get())
            if self.username_entry.get().strip() == '' or self.password_entry.get().strip() == '':
                print("Username or password is empty")
            elif not os.path.exists(user_dir):
                print("User does not exist")
            else:
                with open(os.path.join(user_dir, "local_key.txt"), 'r') as file:
                    password = file.read()
                    password = password.replace('\n', '')
                    if hashlib.sha256(self.password_entry.get().encode()).hexdigest() == password:
                        print("Correct password")
                        self.window.destroy()
                    else:
                        print("Incorrect password")
            self.user_directory = user_dir
        elif window_type == 'Register':
            self.window.destroy()
            self.create_window('Login')

    def register(self, window_type):
        if window_type == 'Register':
            if self.username_entry.get().strip() == '' or self.repeat_password_entry.get().strip() == '' or self.password_entry.get().strip() == '':
                print("Fields can't be empty")
            elif os.path.exists(os.path.join(path, self.username_entry.get())):
                print("User exists")
            else:
                password_hash = hashlib.sha256(self.password_entry.get().encode()).hexdigest()
                repeated_password_hash = hashlib.sha256(self.repeat_password_entry.get().encode()).hexdigest()

                if password_hash == repeated_password_hash:
                    user_dir = os.path.join(path, self.username_entry.get())
                    os.mkdir(user_dir)
                    with open(os.path.join(user_dir, "local_key.txt"), 'w') as file:
                        file.write(password_hash)
                    self.window.destroy()
                    self.create_window('Login')
                else:
                    print("Passwords are not the same")
        elif window_type == 'Login':
            self.window.destroy()
            self.create_window('Register')
