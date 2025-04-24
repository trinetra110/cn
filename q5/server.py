import socket

# Next create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket is created successfully")

# Get local machine name
host = socket.gethostname()

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

    msg = c.recv(1024)
    print(msg.decode())

    # Send some data to the client
    msg = input('Server: ')
    msg = "Server: " + msg
    c.send(msg.encode())

    # Close the connection with the client
    c.close()