
class ClientClass:
    def __init__(self):
            self.username = None
            self.socket = None
            self.room = False       

    def set_username_socket(self, username, socket):
        self.socket = socket
        self.username = username
        message = "  set_username  " + username
        message = str(len(message)) + message + '\n'
        socket.sendall(message.encode('utf-8'))
        #data = socket.recv(1024) 
        #data = data.decode("utf-8")
        #print(data) 

    def list_names(self):
        self.socket.sendall("7  names \n".encode('utf-8'))
        #data = self.socket.recv(1024) 
        #data = data.decode("utf-8")
        #print(data) 

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
        #print(self.username + ": " + message)
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
        self.socket.sendall("7  rooms \n".encode('utf-8'))
        #data = self.socket.recv(1024) 
        #data = data.decode("utf-8")
        #print(data)

    def close_connection(self):
        self.socket.sendall("7  close \n".encode('utf-8'))
        #data = self.socket.recv(1024) 
        #data = data.decode("utf-8")
        #print(data)
    
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
                else:
                    self.message(input)
            else:
                print("Sorry, we didn't understand that command")

    