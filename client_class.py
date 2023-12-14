import asyncio
import os
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import serialization, hashes
# from cryptography.hazmat.primitives.asymmetric import rsa, padding

class ClientClass:
    def __init__(self):
            self.username = None
            self.socket = None
            self.room = False  
            # self.private_key = None
            # self.public_key = None

    def set_username_socket(self, username, socket):
        self.socket = socket
        self.username = username
        message = "  set_username  " + username + "\n"
        message = str(len(message)) + message 
        socket.sendall(message.encode('utf-8'))
        # self.set_key()

    # def set_key(self):
    #     self.private_key = rsa.generate_private_key(
    #         public_exponent=65537,
    #         key_size=2048,
    #         backend=default_backend()
    #     )
    #     self.public_key = self.private_key.public_key()
    #     message =  " public_key " + self.public_key
    #     self.socket.sendall(len(message) + message.encode('utf-8'))

    def list_names(self):
        self.socket.sendall("7  names".encode('utf-8'))

    def list_members(self):
        room_name = input("What room would you like to check the members of?")
        length = len("namesof " + room_name)
        self.socket.sendall((str(length + 1) + " namesof " + room_name).encode('utf-8'))

    def reset_name(self):
        # Resets name on client and server
        name = input("What would you like your new name to be?\n")
        old_name = self.username
        self.username = name
        message = "  reset_name  " + old_name + " " + name 
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))


    def help(self):
        print("""Current commands available:
        names: returns list of all users
        reset: reset your username 
        rooms: lists rooms
        join: joins chatroom
        create: creates a chatroom
        leave: leaves room you are in
        close: closes connection
        send: sends a file (NOT WORKING)
        members: lists members of room
        help: lists all commands""")


    def message(self, message):
        message = "  message  " + self.username + " " + message
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))


    def create_room(self):
        room_name = input("What would you like your room name to be?\n")
        message = "  create  " + self.username + ' ' + room_name
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        print("created room: " + room_name)

    def leave_room(self):
        self.room = False
        message = "  leave  " + self.username
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        print("Left Room")

    def join_room(self):
        room_name = input("What room would you like to join?\n")
        message = "  join  " + self.username + ' ' + room_name
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        self.room = True
        print("Joined room: " + room_name)

    def list_rooms(self):
        self.socket.sendall("7  rooms".encode('utf-8'))

    def close_connection(self):
        self.socket.sendall("7  close".encode('utf-8'))

    def send_file(self):
        file_path = input("What is the path to the file you'd like to send?\n")
        file_name = input("What is the name of the file you'd like to send?\n")
        with open(file_path, 'rb') as file:
            file_data = file.read()

        header = "  file  " + file_name + " " + self.username + " "
        self.socket.sendall((str(len(file_data) + len(header))).encode("utf-8"))
        self.socket.sendall(header.encode("utf-8"))
        self.socket.sendall(file_data)

    
    
    def find_command(self, input):
        #Could add reset name method
        if input == 'names':
            self.list_names()
        elif input == 'reset':
            self.reset_name()
        elif input == 'help':
            self.help()
        elif input == 'create':
            self.create_room()
        elif input == 'join':
            self.join_room()
        elif input == 'rooms':
            self.list_rooms()
        elif input == 'close':
            self.close_connection()
        else:
            if self.room == True:
                if input == 'leave':
                    self.leave_room()
                elif input == 'send':
                    self.send_file()
                elif input == 'members':
                    self.list_members()
                else:
                    self.message(input)
            else:
                print("Sorry, we didn't understand that command")

    
