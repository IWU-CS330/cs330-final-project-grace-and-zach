#client
import socket
import client_class
import threading


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def receive_messages(socket):
    while True:
        data = socket.recv(1024)
        if not data:
            break
        print(f"{data.decode('utf-8')}")

def client_startup(socket):
    client_class.set_socket(socket)
    while True:
        username = input("What is your name\n")
        if username != "":
            break
    s.sendall(client_class.set_username(username))
    client_class.help()
    while True:
        user_input = input("enter a message\n")
        split_input = user_input.split()
        client_class.find_command(split_input[1], split_input[2])

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send_thread = threading.Thread(target=client_startup, args=(s,))
        receive_thread = threading.Thread(target=receive_messages, args=(s,))