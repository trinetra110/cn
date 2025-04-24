# receiver.py
import socket
import random

HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Listening on {HOST}:{PORT}")

expected_frame = 0

while True:
    data, addr = sock.recvfrom(1024)
    frame = data.decode()

    if frame == "exit":
        print("Connection closed.")
        break

    frame_id, content = frame.split(":")
    frame_id = int(frame_id)

    # Simulate frame loss
    if random.random() < 0.2:
        print(f"Frame {frame_id} lost! No ACK sent.")
        continue

    if frame_id == expected_frame:
        print(f"Received Frame {frame_id}: {content}")
        sock.sendto(str(frame_id).encode(), addr)
        expected_frame += 1
    else:
        print(f"Duplicate or out-of-order frame {frame_id}. Resending last ACK.")
        ack_id = expected_frame - 1
        sock.sendto(str(ack_id).encode(), addr)
