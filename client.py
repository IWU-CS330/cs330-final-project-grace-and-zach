import socket
import sqlite3
#client

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    user_name = input("What is your name:")
    while True:
        #user_name = input("What is your name:")
        if user_name == "":
            break
        s.sendall(user_name.encode('utf-8'))
        s.sendall(b"\n")
        data = s.recv(100000000) # when recieving must specify how many bytes to recieve
        data = data.decode("utf-8")


        print(f"Received {data!r}")
        break
        # print here a list of commands or something like that (keep them in the loop until they want to leave the program)