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
lock = threading.Lock()
timers = {}

def send_frame(seq):
    message = f"{seq}:Frame-{seq}"
    sock.sendto(message.encode(), SERVER_ADDR)
    print(f"[Sender] Sent Frame {seq}")
    timers[seq] = time.time()

def timeout_check():
    global base
    while base < TOTAL_FRAMES:
        time.sleep(0.1)
        with lock:
            if base < next_seq:
                if time.time() - timers.get(base, 0) > TIMEOUT:
                    print(f"[Sender] Timeout for Frame {base}. Resending window from {base} to {next_seq - 1}")
                    for i in range(base, next_seq):
                        send_frame(i)

threading.Thread(target=timeout_check, daemon=True).start()

while base < TOTAL_FRAMES:
    with lock:
        while next_seq < base + WINDOW_SIZE and next_seq < TOTAL_FRAMES:
            send_frame(next_seq)
            next_seq += 1

    try:
        ack, _ = sock.recvfrom(1024)
        ack_num = int(ack.decode())
        print(f"[Sender] Received ACK {ack_num}")

        with lock:
            if ack_num >= base:
                # Slide the window
                for i in range(base, ack_num + 1):
                    timers.pop(i, None)
                base = ack_num + 1
    except socket.timeout:
        continue

print("[Sender] All frames sent and acknowledged.")
sock.sendto(b"exit", SERVER_ADDR)
sock.close()
