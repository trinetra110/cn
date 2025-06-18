# 7. Write socket program in Python for multi-client communication using TCP.

import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}  # nickname -> (client_socket, address)

print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

# Handle messages from a specific client
def handle_client(nickname, client):
    client_socket, address = client
    print(f"[CONNECTED] {nickname} at {address}")
    client_socket.send(f"Welcome, {nickname}! Type 'exit' to disconnect.".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                break
            print(f"[{nickname}]: {message}")
        except:
            break

    print(f"[DISCONNECTED] {nickname}")
    client_socket.close()
    del clients[nickname]

# Allow server operator to reply to specific clients
def server_input():
    while True:
        if not clients:
            continue
        print("\n[SERVER MODE] Type: <nickname>: <message>")
        input_data = input()
        if ':' not in input_data:
            print("[ERROR] Use format: nickname: message")
            continue
        target, msg = input_data.split(":", 1)
        target = target.strip()
        msg = msg.strip()

        if target in clients:
            clients[target][0].send(f"Server: {msg}".encode())
        else:
            print(f"[ERROR] No such user '{target}'")

# Accept new clients and start their thread
def accept_clients():
    while True:
        client_socket, address = server.accept()
        client_socket.send("NICKNAME".encode())
        nickname = client_socket.recv(1024).decode()

        clients[nickname] = (client_socket, address)
        thread = threading.Thread(target=handle_client, args=(nickname, clients[nickname]))
        thread.start()

# Start server input thread
threading.Thread(target=server_input, daemon=True).start()

# Start accepting clients
accept_clients()
