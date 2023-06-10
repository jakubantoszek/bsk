# Secure Chat Application

The Secure Chat Application is a client-server chat application that provides secure communication using encryption algorithms. It allows users to exchange encrypted messages and send encrypted files over a network.

Implementation of the project as part of the subject of studies: Security of Computer Systems.

## Authors

- [@jakubantoszek](https://github.com/jakubantoszek)

- [@AgnieszkaDelmaczynska](https://github.com/AgnieszkaDelmaczynska)

## Features

- Secure communication using encryption algorithms (`AES`, `RSA`)
- Choice of encryption modes (`ECB`, `CBC`)
- Sending and receiving encrypted messages
- Sending and receiving encrypted files

## Prerequisites

Before running the Secure Chat Application, make sure you have the following prerequisites installed:

- `Python 3.11`
- `tkinter` library (for GUI)
- `cryptography` library

## Installation

1. Clone the repository to your local machine using the following command:
    `git clone https://github.com/jakubantoszek/bsk.git`
2. Install the required dependencies. Run the following commands:
    `pip install tkinter`
    `pip install cryptography`

## Getting Started
To get started with the Secure Chat Application, follow these steps:
1. Start the server by running the following command:
    `python server.py` or just run the file `server.py`
    
    The server will start listening for incoming connections on the specified host and port.
####
2. Start a client instance by running the following command:
    `python client.py` or just run the file `client.py`
    
    The client application will launch, displaying the main window where you can enter messages or send files securely.

3. Log in using your credentials or create a new account if you don't have one.

4. After successful login and creating connection details, the main window will appear, allowing you to enter messages or send files securely.

## Files

The Secure Chat Application consists of the following files:

- `client.py`: The client-side application responsible for sending and receiving messages/files securely.
- `server.py`: The server-side application responsible for accepting connections and forwarding messages/files between clients.
- `utils.py`: Contains utility functions for encryption, decryption, and key generation.
- `GenerateKey.py`: Allows users to generate RSA key pairs.
- `ConfigureConnection.py`: Allows users to configure the server host and port.
- `Login.py`: Handles user authentication and account creation.
- `MainWindow.py`: Displays the main application window for sending messages and files securely.
- `constants.py`: All the of the variables describing colors, sizes and fonts have been defined in this file.

## Encryption

The Secure Chat Application uses the Advanced Encryption Standard (AES) algorithm for encryption. It supports two modes of operation: Electronic Codebook (ECB) and Cipher Block Chaining (CBC). Users can choose the encryption mode when sending messages or files.

## Documentation

Link to project report on Google Drive:
- https://docs.google.com/document/d/13h5VfgW6aMQsHDP0VQc0_pA3CQdiwPC8FIokmxQ0XK4/edit?usp=sharing

## Contributing

Contributions to the Secure Chat Application are welcome! If you find any issues or have suggestions for improvements, please feel free to contact us on Github :)
