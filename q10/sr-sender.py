import socket
import time
import threading

SERVER_ADDR = ('127.0.0.1', 12345)
WINDOW_SIZE = 4
TOTAL_FRAMES = 10
TIMEOUT = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)

base = 0
next_seq = 0
timers = {}
ack_received = [False] * TOTAL_FRAMES
lock = threading.Lock()

def send_frame(seq):
    msg = f"{seq}:Frame-{seq}"
    sock.sendto(msg.encode(), SERVER_ADDR)
    print(f"[Sender] Sent Frame {seq}")
    timers[seq] = time.time()

def timeout_check():
    while base < TOTAL_FRAMES:
        time.sleep(0.1)
        with lock:
            for seq in range(base, min(base + WINDOW_SIZE, TOTAL_FRAMES)):
                if not ack_received[seq] and time.time() - timers.get(seq, 0) > TIMEOUT:
                    print(f"[Sender] Timeout for Frame {seq}. Resending...")
                    send_frame(seq)

threading.Thread(target=timeout_check, daemon=True).start()

while base < TOTAL_FRAMES:
    with lock:
        while next_seq < base + WINDOW_SIZE and next_seq < TOTAL_FRAMES:
            send_frame(next_seq)
            next_seq += 1

    try:
        ack_data, _ = sock.recvfrom(1024)
        ack_msg = ack_data.decode()

        if ack_msg.startswith("NAK:"):
            nak_seq = int(ack_msg.split(":")[1])
            print(f"[Sender] Received NAK for Frame {nak_seq}. Resending...")
            with lock:
                send_frame(nak_seq)
        else:
            ack_seq = int(ack_msg)
            print(f"[Sender] Received ACK {ack_seq}")
            with lock:
                if not ack_received[ack_seq]:
                    ack_received[ack_seq] = True
                    timers.pop(ack_seq, None)
                    while base < TOTAL_FRAMES and ack_received[base]:
                        base += 1

    except socket.timeout:
        continue

print("[Sender] All frames acknowledged. Exiting...")
sock.sendto(b"exit", SERVER_ADDR)
sock.close()
