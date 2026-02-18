import socket
import json
import time
import random

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = {
        "id": 1,
        "ax": random.uniform(-2, 2),
        "ay": random.uniform(-2, 2),
        "az": random.uniform(8, 10)
    }

    sock.sendto(json.dumps(message).encode(), (UDP_IP, UDP_PORT))
    print("Sent:", message)

    time.sleep(0.5)