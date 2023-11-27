
class ClientClass:
    def __init__(self):
            self.username = None
            self.socket = None
            self.room = False       

    def set_username_socket(self, username, socket):
        self.socket = socket
        self.username = username
        #print(username)
        message = "  set_username  " + username
        message = str(len(message)) + message + '\n'
        socket.sendall(message.encode('utf-8'))
        data = socket.recv(1024) 
        data = data.decode("utf-8")
        print(data) 
        

    def list_names(self):
        self.socket.sendall("7  names".encode('utf-8'))
        data = socket.recv(1024) 
        data = data.decode("utf-8")
        print(data) 

    def help(self):
        print("""Current commands available:
        names: returns list of all users
        rooms: lists rooms
        join: joins chatroom
        create: creates a chatroom
        leave: leaves room you are in
        close: closes connection
        help: lists all commands""")

    def message(self, message):
        message = "  message  " + self.username + ": " + message
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))
        print(self.username + ": " + message)

    def create_room(self, room_name):
        message = "  create  " + self.username + ' ' + room_name
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        print("created room: " + room_name)

    def leave_room(self):
        self.room = False
        message = "  leave  " + self.username
        message = str(len(message)) + message
        self.socket.sendall(message.encode('utf-8'))
        print("Left Room")

    def join_room(self, message):
        self.room = True
        message = "  join  " + self.username + ' ' + message
        message = str(len(message)) + message + "\n"
        self.socket.sendall(message.encode('utf-8'))
        print("Joined room: " + message)

    def list_rooms(self):
        self.socket.sendall("7  rooms".encode('utf-8'))
        data = socket.recv(1024) 
        data = data.decode("utf-8")
        print(data)

    def close_connection(self):
        self.socket.sendall("7  close".encode('utf-8'))
    
    def find_command(self, input, message):
        #Could add reset name method
        if input == 'names':
            self.list_names()
        elif input == 'help':
            self.help()
        elif input == 'create':
            self.create_room(message)
        elif input == 'join':
            self.join_room(message)
        elif input == 'rooms':
            self.list_rooms()
        elif input == 'close':
            self.close_connection()
        else:
            if self.room == True:
                if input == 'leave':
                    self.leave_room(message)
                else:
                    self.message(input + message)
            else:
                print("Sorry, we didn't understand that command")

    