#client
import socket
import client_class
import threading


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 59898  # The port used by the server

def receive_messages(socket, client):
    # Handles receiving messages for the client
    # First waits for an initial length of a message, then listens for the rest of that length
    # After getting message, splits it and checks against possibilites
    while True:
        data_length = socket.recv(4)
        if not data_length:
            break
        data = socket.recv(int(data_length))
        data = data.decode('utf-8')
        if not data:
            break
        split_data = data.split()

        # Updates the users list of other user's keys in the room
        if split_data[0] == 'get_public_keys':
            client.public_keys = []
            for value in split_data[1:]:
                client.public_keys.append(value)

        # Handles the unique protocol for files
        # Files are very long, and its better to recieve the actual file with its own length
        # Files like messages must be decrypted
        elif split_data[0] == 'file':
            file_length = socket.recv(6)
            file_data = socket.recv(int(file_length))
            file_data = file_data.decode('utf-8')
            file_data = client.decrypt_message(file_data)

            with open(split_data[2], 'wb') as received_file:
                received_file.write(file_data)
            print(split_data[1], " Sent file: ", split_data[2])

        # Standard decryption for printing a message
        elif split_data[0] == 'message':
            decrypted_message = client.decrypt_message(split_data[2])
            print(split_data[1], ": ", decrypted_message)

        # Otherwise just prints whatever is recieved from server
        else:
            print(data)

def client_startup(socket, client):
    # Handles beginning of program, asking for users name and getting the client states setup
    username = input("What is your name\n")
    client.set_username_socket(username, socket)
    client.help()
    # Runs loop endlessly ready for user input
    while True:
        user_input = input("\n")
        client.find_command(user_input)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, 59898)) 
        client = client_class.ClientClass()
        send_thread = threading.Thread(target=client_startup, args=(s,client,))
        receive_thread = threading.Thread(target=receive_messages, args=(s,client,))
        send_thread.start()
        receive_thread.start()
        send_thread.join()
        receive_thread.join()
