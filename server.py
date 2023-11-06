# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#HOST  = "0.0.0.0" #Listen to all interfaces
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    #while True:
    conn, addr = s.accept()
    #conn is another socket object for new incoming connection
    # addr is client address
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)