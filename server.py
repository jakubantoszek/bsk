import threading

from MainWindow import MainWindow
from GenerateKey import GenerateKey
from ConfigureConnection import ConfigureConnection
from Login import Login


if __name__ == '__main__':
    login = Login()
    generate_key = GenerateKey(login.user_directory, login.password)
    generate_key.window.mainloop()

    configure_connection = ConfigureConnection("server", login.user_directory)
    configure_connection.window.mainloop()
    configure_connection.user_socket.close()
