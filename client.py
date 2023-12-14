#client
import socket
import client_class
import threading


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 59898  # The port used by the server

def receive_messages(socket):
    while True:
        data_length = socket.recv(6)
        #print("here is the data length:", data_length)
        data = socket.recv(int(data_length.decode("utf-8")))
        data = data.decode('utf-8')
        if not data:
            break
        split_data = data.split()
        print("split_Data:", split_data)
        if split_data[0] == 'file':
            with open(split_data[1], 'wb') as received_file:
                #This may not work with file data
               data_length = socket.recv(20)
             #print("here is the data length:", data_length)
               data = socket.recv(int(data_length.decode("utf-8")))
               for x in data:
                    received_file.write(x)
        else:
            print(data)
        

def client_startup(socket):
    client = client_class.ClientClass()
    username = input("What is your name\n")
    client.set_username_socket(username, socket)
    client.help()
    while True:
        user_input = input("\n")
        client.find_command(user_input)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, 59898)) 
        send_thread = threading.Thread(target=client_startup, args=(s,))
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        send_thread.start()
        receive_thread.start()
        send_thread.join()
        receive_thread.join()
        #client_startup(s)
