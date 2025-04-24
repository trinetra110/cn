import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICKNAME':
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("Disconnected from server.")
            client.close()
            break

def write():
    while True:
        msg = input()
        if msg.lower() == 'exit':
            client.send('exit'.encode())
            client.close()
            break
        client.send(msg.encode())

threading.Thread(target=receive).start()
threading.Thread(target=write).start()
