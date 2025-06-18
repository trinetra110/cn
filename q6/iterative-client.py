# 6. Write chat program in Python using TCP with the help of an iterative server.

import socket
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get local machine name
host = socket.gethostname()
name = input("Enter your name: ")
# Define the port on which we want to connect
port = 23456

# connect to the server on local computer
s.connect((host, port))

while True:
    # Send some data to the server
    msg = input(name + ': ')
    msgf = name + ': ' + msg
    s.send(msgf.encode())
    if msg.lower().strip() == 'exit':
        break
    
    # Receive data from the server
    msg = s.recv(1024)
    print(msg.decode())

# Close the connection
s.close()