# receiver_stop_and_wait.py
import socket
import random

HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"[Receiver] Listening on {HOST}:{PORT}")

expected_frame = 0

while True:
    data, addr = sock.recvfrom(1024)
    frame = data.decode()

    if frame == "exit":
        print("[Receiver] Connection closed.")
        break

    frame_id, content = frame.split(":")
    frame_id = int(frame_id)

    # Simulate frame loss (just log it, don't handle it)
    if random.random() < 0.2:
        print(f"[Receiver] Frame {frame_id} lost/corrupted. Not processed.")
        continue

    if frame_id == expected_frame:
        print(f"[Receiver] Received Frame {frame_id}: {content}")
        sock.sendto(str(frame_id).encode(), addr)
        expected_frame += 1
    else:
        print(f"[Receiver] Out-of-order frame {frame_id}. Ignoring.")
