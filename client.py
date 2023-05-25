from MainWindow import MainWindow
from GenerateKey import GenerateKey
from ConfigureConnection import ConfigureConnection
from Login import Login


if __name__ == '__main__':
    login = Login()
    generate_key = GenerateKey()
    generate_key.window.mainloop()

    configure_connection = ConfigureConnection("client")
    configure_connection.window.mainloop()

    root = MainWindow(configure_connection.address, 8080)
    root.window.mainloop()

    configure_connection.user_socket.close()
