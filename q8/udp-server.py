# 8. Write socket program in Python to send a message from a client machine to a server machine using UDP.

import socket

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Changed to SOCK_DGRAM
print("Socket is created successfully")

host = socket.gethostname()
port = 23456

# Bind to the port
s.bind((host, port))
print(f"Socket is binded to {port}")

print("Socket is ready to receive messages")

while True:
    # Receive data from client
    msg, addr = s.recvfrom(1024)  # Changed to recvfrom
    msg_str = msg.decode()
    print(msg_str)
    
    msg_str = msg_str.split(':')
    if msg_str[1].lower().strip() == 'exit':
        print(f"{msg_str[0]} {addr} disconnected")
        continue
    
    # Send response
    response = input("Server: ")
    s.sendto(f"Server: {response}".encode(), addr)  # Changed to sendto