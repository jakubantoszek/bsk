from MainWindow import MainWindow
from GenerateKey import GenerateKey
from ConfigureConnection import ConfigureConnection
from Login import Login
from utils import get_session_key, session_keys_exchange


if __name__ == '__main__':
    # Login and get or generate keys (if they don't exist)
    login = Login()
    generate_key = GenerateKey(login.user_directory, login.password)
    generate_key.window.mainloop()

    # Connect with server
    configure_connection = ConfigureConnection("client", generate_key.public_key)
    configure_connection.window.mainloop()

    # Get session keys for two-way communication
    session_key = get_session_key(configure_connection.other_client_key)
    session_key_2 = session_keys_exchange(configure_connection.socket,
                                          session_key)

    # Create main window to send and receive files/messages
    root = MainWindow(session_key, session_key_2, configure_connection.socket,
                      login.user_directory)
    root.window.mainloop()

    # Finish the connection to the server
    configure_connection.socket.close()
