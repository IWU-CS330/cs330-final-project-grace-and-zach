from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class ClientClass:
    def __init__(self):
            self.username = None
            self.socket = None
            self.room = False  
            self.private_key = None

    def set_username_socket(self, username, socket):
        self.socket = socket
        self.username = username
        message = "  set_username  " + username + '\n'
        message = str(len(message)) + message 
        socket.sendall(message.encode('utf-8'))
        self.set_key()

    def set_key(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        message =  " set_public_key " + self.username + self.private_key.public_key()
        message = str(len(message)) + message 
        self.socket.sendall(message.encode('utf-8'))

    def list_names(self):
        self.socket.sendall("7  names \n".encode('utf-8'))

    def help(self):
        print("""Current commands available:
        names: returns list of all users
        rooms: lists rooms
        join: joins chatroom
        create: creates a chatroom
        leave: leaves room you are in
        close: closes connection
        file: sends a file
        help: lists all commands""") 

    def create_room(self):
        room_name = input("What would you like your room name to be?\n")
        message = "  create  " + self.username + ' ' + room_name
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        print("Created room: " + room_name)

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
        self.socket.sendall("7  rooms \n".encode('utf-8'))

    def close_connection(self):
        self.socket.sendall("7  close \n".encode('utf-8'))

    def message(self, input):
        public_key_list = self.socket.sendall("16 get_public_keys".encode('utf-8'))
        for key in public_key_list:
            message = key.encrypt(
                input,
                padding.PKCS1v15()
            )
            message = "message  " + self.username + " " + message
            message = str(len(message)) + message + "\n"
            self.socket.sendall(message.encode('utf-8')) 
    
    def send_file(self):
        file_path = input("What is the path to the file you'd like to send?\n")
        file_name = input("What is the name of the file you'd like to send?\n")
        with open(file_path, 'rb') as file:
            file_data = file.read()
        public_key_list = self.socket.sendall("16 get_public_keys".encode('utf-8'))
        for key in public_key_list:
            message = key.encrypt(
                file_data,
                padding.PKCS1v15()
            )
            header = "file " + self.username + " " + file_name
            self.socket.sendall(len(header) + header)
            self.socket.sendall(len(message) + message)
    
    def decrypt_message(self, input):
        decrypted_message = self.private_key.decrypt(
            input,
            padding.PKCS1v15()
        )
        return decrypted_message

    def find_command(self, input):
        #Could add reset name method
        if input == 'names':
            self.list_names()
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
                else:
                    self.message(input)
            else:
                print("Sorry, we didn't understand that command")

    