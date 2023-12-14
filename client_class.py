from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class ClientClass:
    def __init__(self):
            self.username = None
            self.socket = None
            self.room = False  
            self.private_key = None
            self.public_keys = []

    def set_username_socket(self, username, socket):
        # Sets up the states of the class to include the socket, and username
        # Also calls set key to continue setup
        self.socket = socket
        self.username = username
        message = "  set_username  " + username + "\n"
        message = str(len(message)) + message 
        socket.sendall(message.encode('utf-8'))
        self.set_key()

    def set_key(self):
        # Sets private key, and sends public key to the server
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        message =  " set_public_key " + self.username + str(self.private_key.public_key())
        message = str(len(message)) + message 
        self.socket.sendall(message.encode('utf-8'))

    def decrypt_message(self, input):
        # Decrypts message
        decrypted_message = self.private_key.decrypt(
            input,
            padding.PKCS1v15()
        )
        return decrypted_message

    def help(self):
        print("""Current commands available:
        names: returns list of all users
        reset: resets username
        create: creates a chatroom
        rooms: lists rooms
        join: joins chatroom
        members: lists members of room
        file: sends a file
        leave: leaves room you are in
        close: closes connection
        send: sends a file
        members: lists members of room
        help: lists all commands""")

    def list_names(self):
        self.socket.sendall("7 names".encode('utf-8'))
    
    def list_members(self):
        self.socket.sendall("7 namesof".encode('utf-8'))

    def reset_name(self):
        # Resets name on client and server
        name = input("What would you like your new name to be?\n")
        self.username = name
        message = "  reset_name  " + name + "\n"
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))

    def create_room(self):
        # Tells server to create room with the name of the input
        room_name = input("What would you like your room name to be?\n")
        message = "  create  " + self.username + ' ' + room_name
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        print("Created room: " + room_name)

    def join_room(self):
        # Joins room of the given input, and also gets the public keys
        room_name = input("What room would you like to join?\n")
        message = "  join  " + self.username + ' ' + room_name
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        self.socket.sendall("16 get_public_keys".encode('utf-8'))
        self.room = True
        print("Joined room: " + room_name)

    def list_rooms(self):
        self.socket.sendall("7  rooms".encode('utf-8'))

    def close_connection(self):
        self.socket.sendall("7  close".encode('utf-8'))
    
    def message(self, message):
        self.socket.sendall(("50 get_public_keys " + self.username).encode('utf-8'))
        for key in self.public_keys:
            encrypted_message = key.encrypt(
                input,
                padding.PKCS1v15()
            )
            message = "  message  " + self.username + ": " + encrypted_message
            message = str(len(message)) + message + "\n"
            self.socket.sendall(message.encode('utf-8'))

    def send_file(self):
        # Finds the path and name of the file, then encrypts with available public keys
        # Then sends the unique encrypted file to its intended recievers 1 by 1
        #self.socket.sendall("16 get_public_keys".encode('utf-8'))
        file_path = input("What is the path to the file you'd like to send?\n")
        file_name = input("What is the name of the file you'd like to send?\n")
        with open(file_path, 'rb') as file:
            file_data = file.read()
        for key in self.public_keys:
            message = key.encrypt(
                file_data,
                padding.PKCS1v15()
            )
            header = " file " + self.username + " " + file_name
            self.socket.sendall(len(header) + header)
            self.socket.sendall(len(message) + message)
    
    def leave_room(self):
        # Leaves room, adjusts state accordingly
        message = "  leave  " + self.username
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        self.room = False
        self.public_keys = []
        print("Left Room")


    def find_command(self, input):
        # Handles input from the user to call the correct function
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
                elif input == 'members':
                    self.list_members()
                elif input == 'send':
                    self.send_file()
                elif input == 'members':
                    self.list_members()
                else:
                    self.message(input)
            else:
                print("Sorry, we didn't understand that command")
