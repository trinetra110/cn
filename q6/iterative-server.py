# 6. Write chat program in Python using TCP with the help of an iterative server.

import socket

# Next create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket is created successfully")

# Get local machine name
host = socket.gethostname()
name = "Server: "
# Reserve a port on the computer in this case it is 23456 but it can be anything
port = 23456

# Next bind to the port
s.bind((host, port))
print ("Socket is binded to %s" %(port))

# Put the socket into listening mode
s.listen(5)
print ("Socket is listening")

# A forever loop until we interrupt it or an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print ('Got connection from', addr )

    while True:
        # Receive the data from the client
        msg = c.recv(1024)
        msgf = msg.decode().split(':')
        if msgf[1].strip().lower() == 'exit':
            print(msgf[0] + ' disconnected')
            break
        print(msg.decode())

        # Send some data to the client
        msg = input('Server: ')
        msg = name + msg
        c.send(msg.encode())

    # Close the connection with the client
    c.close()