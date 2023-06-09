import os.path
import hashlib
import tkinter as tk

from constants import *
#path = "H:\\Studia\\Semestr 6\\bsk_users"
path = 'C:\\bsk'


class Login:
    def __init__(self):
        self.password = None
        self.repeat_password_entry = None
        self.repeat_password_label = None
        self.register_button = None
        self.password_entry = None
        self.login_button = None
        self.username_entry = None
        self.password_label = None
        self.username_label = None
        self.user_directory = None
        self.message_label = None

        self.create_window('Login')
        self.window.mainloop()


    def create_window(self, window_type):
        self.window = tk.Tk()
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=BACKGROUND_COLOR_DARKER)

        if window_type == 'Login':
            self.window.title("Login")
            self.login_window()
        elif window_type == 'Register':
            self.window.title("Register")
            self.register_window()


    def login_window(self):
        login_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR, padx=20, pady=20)
        login_frame.pack(pady=20)

        title_label = tk.Label(login_frame, text="Login", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1)
        title_label.pack(pady=10)

        form_frame = tk.Frame(login_frame, bg=BACKGROUND_COLOR, padx=10, pady=10)
        form_frame.pack(pady=10)

        self.username_label = tk.Label(form_frame, text="Username:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR, fg=TEXT_COLOR2)
        self.username_label.pack()

        self.username_entry = tk.Entry(form_frame, font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.username_entry.pack()

        self.password_label = tk.Label(form_frame, text="Password:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR, fg=TEXT_COLOR2)
        self.password_label.pack()

        self.password_entry = tk.Entry(form_frame, show="*", font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.password_entry.pack()

        self.login_button = tk.Button(login_frame, text="Login", command=lambda: self.login('Login'), font=BUTTON_FONT, bg=BUTTON_COLOR1, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1, width=7)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(login_frame, text="Register", command=lambda: self.register('Login'), font=BUTTON_FONT, bg=BUTTON_COLOR2, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR2)
        self.register_button.pack()

        self.message_label = tk.Label(login_frame, text="", font=LABEL_FONT, fg=ERROR_COLOR, bg=BACKGROUND_COLOR)
        self.message_label.pack(pady=10)


    def register_window(self):

        register_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR, padx=20, pady=20)
        register_frame.pack(pady=20)

        title_label = tk.Label(register_frame, text="Register", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR1)
        title_label.pack(pady=10)

        form_frame = tk.Frame(register_frame, bg=BACKGROUND_COLOR, padx=10, pady=10)
        form_frame.pack(pady=10)

        self.username_label = tk.Label(form_frame, text="Username:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR, fg=TEXT_COLOR2)
        self.username_label.pack()

        self.username_entry = tk.Entry(form_frame, font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.username_entry.pack()

        self.password_label = tk.Label(form_frame, text="Password:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR, fg=TEXT_COLOR2)
        self.password_label.pack()

        self.password_entry = tk.Entry(form_frame, show="*", font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.password_entry.pack()

        self.repeat_password_label = tk.Label(form_frame, text="Repeat password:", font=LABEL_FONT_BOLD, bg=BACKGROUND_COLOR, fg=TEXT_COLOR2)
        self.repeat_password_label.pack()

        self.repeat_password_entry = tk.Entry(form_frame, show="*", font=LABEL_FONT, bg=ENTRY_BACKGROUND_COLOR, fg=ENTRY_TEXT_COLOR)
        self.repeat_password_entry.pack()

        self.register_button = tk.Button(register_frame, text="Register", command=lambda: self.register('Register'), font=BUTTON_FONT, bg=BUTTON_COLOR1, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR1)
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(register_frame, text="Login", command=lambda: self.login('Register'), font=BUTTON_FONT, bg=BUTTON_COLOR2, fg=BUTTON_TEXT_COLOR, activeforeground=BUTTON_TEXT_COLOR2, width=7)
        self.login_button.pack()

        self.message_label = tk.Label(register_frame, text="", font=LABEL_FONT, fg=ERROR_COLOR, bg=BACKGROUND_COLOR)
        self.message_label.pack(pady=10)


    def login(self, window_type):
        if window_type == 'Login':
            user_dir = os.path.join(path, self.username_entry.get())
            if self.username_entry.get().strip() == '' or self.password_entry.get().strip() == '':
                self.show_message("Fields can't be empty")
            elif not os.path.exists(user_dir):
                self.show_message("User does not exist")
            else:
                with open(os.path.join(user_dir, "local_key.txt"), 'r') as file:
                    password = file.read()
                    password = password.replace('\n', '')
                    if hashlib.sha256(self.password_entry.get().encode()).hexdigest() == password:
                        self.show_message("Correct password")
                        self.window.destroy()
                        self.password = password
                    else:
                        self.show_message("Incorrect password")
            self.user_directory = user_dir
        elif window_type == 'Register':
            self.window.destroy()
            self.create_window('Login')


    def register(self, window_type):
        if window_type == 'Register':
            if self.username_entry.get().strip() == '' or self.repeat_password_entry.get().strip() == '' or self.password_entry.get().strip() == '':
                self.show_message("Fields can't be empty")
            elif os.path.exists(os.path.join(path, self.username_entry.get())):
                self.show_message("User exists")
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
                    self.show_message("Passwords are not the same")
        elif window_type == 'Login':
            self.window.destroy()
            self.create_window('Register')


    def show_message(self, message):
        if self.message_label:
            self.message_label.destroy()

        frame = self.window if self.window.title() == "Registration" else self.window.children['!frame']
        self.message_label = tk.Label(frame, text=message, font=LABEL_FONT_MINI, fg=ERROR_COLOR, bg=BACKGROUND_COLOR)
        self.message_label.pack(pady=10)
