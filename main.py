from MainWindow import MainWindow
from GenerateKey import GenerateKey


if __name__ == '__main__':
    generate_key = GenerateKey()
    generate_key.window.mainloop()
    root = MainWindow()
    root.window.mainloop()
