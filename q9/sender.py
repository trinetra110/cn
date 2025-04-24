# sender_stop_and_wait.py
import socket
import time

HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)  # for waiting on ACK

frames = ["A", "B", "C", "D", "E"]

print("[Sender] Starting basic Stop-and-Wait (no ARQ)...\n")

for i, frame in enumerate(frames):
    msg = f"{i}:{frame}"
    sock.sendto(msg.encode(), (HOST, PORT))
    print(f"[Sender] Sent Frame {i}: {frame}")

    try:
        ack_data, _ = sock.recvfrom(1024)
        ack = int(ack_data.decode())
        if ack == i:
            print(f"[Sender] Received ACK {ack}\n")
        else:
            print(f"[Sender] Received out-of-sync ACK {ack}\n")
    except socket.timeout:
        print(f"[Sender] No ACK received for frame {i}\n")

# End communication
sock.sendto("exit".encode(), (HOST, PORT))
sock.close()
