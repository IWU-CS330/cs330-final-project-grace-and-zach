import socket
#client

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    user_input = input("What would you like to say?")
    s.sendall(user_input.encode('utf-8'))
    s.sendall(b"\n")
    if user_input == "":
        s.sendall(b"\n")
    data = s.recv(1024) # when recieving must specify how many bytes to recieve
    data = data.decode("utf-8")


print(f"Received {data!r}")