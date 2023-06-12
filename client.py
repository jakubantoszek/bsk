from MainWindow import MainWindow
from GenerateKey import GenerateKey
from ConfigureConnection import ConfigureConnection
from Login import Login
from utils import get_session_key, session_keys_exchange


if __name__ == '__main__':
    login = Login()
    generate_key = GenerateKey(login.user_directory, login.password)
    generate_key.window.mainloop()

    configure_connection = ConfigureConnection("client", login.user_directory,
                                               generate_key.public_key)
    configure_connection.window.mainloop()

    session_key = get_session_key(configure_connection.other_client_key)
    session_key_2 = session_keys_exchange(configure_connection.socket,
                                          session_key)

    root = MainWindow(session_key, session_key_2, configure_connection.socket,
                      login.user_directory)
    root.window.mainloop()

    configure_connection.user_socket.close()
