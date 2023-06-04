from MainWindow import MainWindow
from GenerateKey import GenerateKey
from ConfigureConnection import ConfigureConnection
from Login import Login
from utils import get_session_key


if __name__ == '__main__':
    login = Login()
    generate_key = GenerateKey(login.user_directory, login.password)
    generate_key.window.mainloop()

    configure_connection = ConfigureConnection("client", login.user_directory,
                                               generate_key.public_key)
    configure_connection.window.mainloop()
    session_key = get_session_key(configure_connection.other_client_key)

    root = MainWindow(configure_connection.address, 8080, session_key,
                      configure_connection.socket)
    root.window.mainloop()

    configure_connection.user_socket.close()
