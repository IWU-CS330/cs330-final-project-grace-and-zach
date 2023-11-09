import socket
#client

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        user_name = input("What is your name\n")
        if user_name != "":
            break
    s.sendall(user_name.encode('utf-8'))
    s.sendall(b"\n")
    data = s.recv(1024) # when recieving must specify how many bytes to recieve
    data = data.decode("utf-8")
    while True:
        user_input = input("enter a message\n")
        if(user_input == "close"):
            break
        s.sendall(user_name.encode('utf-8'))
        s.sendall(b"\n")
        data = s.recv(1024) # when recieving must specify how many bytes to recieve
        data = data.decode("utf-8")

    s.close()