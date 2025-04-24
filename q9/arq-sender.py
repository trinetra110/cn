# sender.py
import socket

HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # timeout in seconds

frames = ["A", "B", "C", "D", "E"]

print("Starting Stop-and-Wait ARQ...\n")

for i, frame in enumerate(frames):
    msg = f"{i}:{frame}"
    while True:
        sock.sendto(msg.encode(), (HOST, PORT))
        print(f"Sent Frame {i}: {frame}")

        try:
            ack_data, _ = sock.recvfrom(1024)
            ack = int(ack_data.decode())
            if ack == i:
                print(f"Received ACK {ack}\n")
                break
            else:
                print(f"Received duplicate ACK {ack}, resending frame {i}...")
        except socket.timeout:
            print(f"Timeout! Resending frame {i}...\n")

# Send exit signal to stop receiver gracefully
sock.sendto("exit".encode(), (HOST, PORT))
sock.close()
