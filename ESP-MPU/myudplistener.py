import socket

UDP_IP = ""   # Listen on all interfaces
UDP_PORT = 61000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening...")
while True:
    data, addr = sock.recvfrom(1024)  # buffer size
    print(data.decode())
