import socket
import random

HOST = '127.0.0.1'
PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

RECEIVE_WINDOW = 4
expected_base = 0
received = {}

print("[Receiver] Ready to receive...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode()

    if msg == "exit":
        print("[Receiver] Connection closed.")
        break

    try:
        seq_str, content = msg.split(":")
        seq = int(seq_str)
    except:
        continue

    if random.random() < 0.1:
        print(f"[Receiver] Frame {seq} lost (simulated). Sending NAK.")
        sock.sendto(f"NAK:{seq}".encode(), addr)
        continue

    if expected_base <= seq < expected_base + RECEIVE_WINDOW:
        if seq not in received:
            received[seq] = content
            print(f"[Receiver] Received Frame {seq}: {content}")
        else:
            print(f"[Receiver] Duplicate Frame {seq}. Resending ACK.")

        sock.sendto(str(seq).encode(), addr)

        # Check for missing frames and send NAKs
        for i in range(expected_base, seq):
            if i not in received:
                print(f"[Receiver] Detected missing frame {i}. Sending NAK.")
                sock.sendto(f"NAK:{i}".encode(), addr)

        while expected_base in received:
            expected_base += 1
    else:
        print(f"[Receiver] Frame {seq} out of window. Ignored.")
