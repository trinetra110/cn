import socket

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Changed to SOCK_DGRAM

host = socket.gethostname()
port = 23456
name = input("Enter your name: ")

while True:
    # Send message to server
    msg = input(name + ': ')
    s.sendto(f"{name}: {msg}".encode(), (host, port))  # Changed to sendto
    
    if msg.lower().strip() == 'exit':
        break
    
    # Receive response from server
    msg, _ = s.recvfrom(1024)  # Changed to recvfrom
    print(msg.decode())

s.close()