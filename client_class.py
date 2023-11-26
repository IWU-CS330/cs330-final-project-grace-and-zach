#class clientclass:
import socket

class clientclass:
    def __init__(self):
            self.self.username = None
            self.socket = None
            self.room = False       

    def set_username_socket(self, username, socket):
        self.socket = socket
        self.username = username
        self.username = "  set_username  " + self.username
        self.username = str(len(self.username)) + self.username
        self.socket.sendall(self.username.encode('utf-8')) 

    def list_names(self):
        self.socket.sendall("7  names".encode('utf-8'))

    def help(self):
        print("""Current commands available:
        names: returns list of all users
        rooms: lists rooms
        join: joins chatroom
        create: creates a chatroom
        add: adds user to your room
        leave: leaves room you are in
        close: closes connection
        help: lists all commands""")

    def message(self, message):
        message = "  message  " + self.username + ": " + message
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))

    def create_room(self, room_name):
        self.room = True
        message = "  create  " + self.username + ' ' + room_name
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))

    def add_user(self, message):
        message = "  add  " + self.username + message
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))

    def leave_room(self):
        self.room = False
        message = "  leave  " + self.username
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))

    def join_room(self, message):
        self.room = True
        message = "  join  " + self.username + ' ' + message
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))

    def list_rooms(self):
        self.socket.sendall("7  rooms".encode('utf-8'))

    def close_connection(self):
        self.socket.sendall("7  close".encode('utf-8'))
    
    def find_command(self, input, message):
        #Could add reset name method
        if input == 'names':
            clientclass.list_names()
        elif input == 'help':
            clientclass.help()
        elif input == 'create':
            clientclass.create_room(message)
        elif input == 'add':
            clientclass.add_user(message)
        elif input == 'join':
            clientclass.join_room(message)
        elif input == 'rooms':
            clientclass.list_rooms()
        elif input == 'close':
            clientclass.close_connection()
        else:
            if self.room == True:
                if input == 'leave':
                    clientclass.leave_room(message)
                else:
                    clientclass.message(input + message)
            else:
                print("Sorry, we didn't understand that command")

    