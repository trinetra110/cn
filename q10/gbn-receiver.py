import socket
import random

HOST = '127.0.0.1'
PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

expected = 0

print("[Receiver] Ready to receive...")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    if message == "exit":
        print("[Receiver] Connection closed.")
        break

    try:
        seq_str, content = message.split(":")
        seq = int(seq_str)
    except:
        continue

    if random.random() < 0.1:  # Simulate 10% frame loss
        print(f"[Receiver] Frame {seq} lost (simulated).")
        continue

    if seq == expected:
        print(f"[Receiver] Received Frame {seq}: {content}")
        sock.sendto(str(seq).encode(), addr)
        expected += 1
    else:
        print(f"[Receiver] Out-of-order Frame {seq}. Discarding. Last ACK: {expected-1}")
        sock.sendto(str(expected - 1).encode(), addr)  # Resend last ACK
