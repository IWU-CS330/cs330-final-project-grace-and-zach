import socket
import client_class
#client

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        user_name = input("What is your name\n")
        if user_name != "":
            break
    s.sendall(client_class.set_username(user_name))
    #s.sendall(b"\n")
    
    data = s.recv(1024) # when recieving must specify how many bytes to recieve
    data = data.decode("utf-8")
    print(data)
    s.sendall(client_class.names())
    data = s.recv(1024)
    data = data.decode("utf-8")
    print("Here is a list of usernames from our current users:", data)
    print(client_class.help())
    while True:
        user_input = input("enter a message\n")
        if(user_input == "close"):
            s.sendall(client_class.close_connection())
            print("Connection Closed")
            break
        elif(user_input == "names"):
            s.sendall(client_class.names())
            data = s.recv(1024)
            data = data.decode("utf-8")
            print("Here is a list of usernames from our current users:", data)
        elif(user_input == "help"):
            print(client_class.help())
        else:
            s.sendall(client_class.message(user_input).encode('utf-8'))
            s.sendall(b"\n")
            data = s.recv(1024) # when recieving must specify how many bytes to recieve
            data = data.decode("utf-8")

    s.close()