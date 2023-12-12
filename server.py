import socket
import sqlite3
import socketserver
import threading

import socketserver
import threading
import sys


#Some of this code about socket programming comes from https://realpython.com/python-sockets/#echo-client-and-server

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

# these next 6 lines of code came from   
# https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python
# they were used to intialize,create, and read the database


with open('names.sql', 'r') as schema:
            script = schema.read()

db = sqlite3.connect('names.db', check_same_thread=False)
cur = db.cursor()
cur.executescript(script)
db.commit()

Dict = {}

def set_username(input):
    if input[0] == 'set_username':
        name = str(input[1])
        db.execute('INSERT INTO names (username, chat_name) VALUES (?,?)', [name, "N/A"])
        db.commit()

        lock = threading.Lock()
            #locked_thread = self.wfile.lock.acquire()
        
        return lock, name
    else:
        return None, None
    

def names(input):
    if input[0] == 'names':
        cur = db.execute('SELECT username from names')
        list_message = ""
        count = 0
        for username in cur.fetchall():
            username = username[0]
            print(username)            
            if len(cur.fetchall()) == 1 or count == len(cur.fetchall()):
                list_message = list_message + username 
            else:
                list_message = username + "," + list_message
            count = count + 1
                
        list_message = "Here is a list of all current users:" + list_message
        
        return list_message  
    
    else:
        return None

def message(input):
    if input[0] == 'message':         
        name = input[1]
        print("Here is the user's name:", name)
        select_room = db.execute('SELECT chat_name from names WHERE username = ?', [name])
        #print("Here is the room", name, "is in:", select_room.fetchall())
        
        for chatroom in select_room.fetchall():
            chatroom = chatroom[0]
        
        chatroom = str(chatroom)
        print(str(chatroom))
        
        select_users = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])

        for user in select_users.fetchall():
            user = user[0]
            print("User:", user)
            
            user_lock = Dict[user][1]
            if user != name:
                with user_lock:
                    user_message = ""
                    
                    for x in range(len(input)):
                        if x >= 2:
                            user_message = user_message + " " + input[x]
                    
                    length = len(name + ":" + user_message)
                    Dict[user][0].write(str(length).encode('utf-8'))
                    Dict[user][0].write((name + ":" + user_message).encode('utf-8'))
                    print("Sent message = ", user_message)

def create(input):
    if input[0] == 'create':
        chatroom = str(input[2])
        db.execute('INSERT INTO chatrooms (chat_name) VALUES (?)', [chatroom])
        db.commit()

def join(input):
    if input[0] == 'join':
        chatroom = str(input[2])
        cur = db.execute('SELECT chat_name from chatrooms WHERE chat_name = ?', [chatroom])
        if cur.fetchall() != []:
            db.execute('UPDATE names SET chat_name = ? WHERE username = ?', [chatroom, str(input[1])])
            db.commit()
            print("help pls")
            return True
        
        else:
            return False
        
    return None
        

def rooms(input):
    if input[0] == 'rooms':
        cur = db.execute('SELECT chat_name from chatrooms')
        list_message = ""
        count = 0
        for chatroom in cur.fetchall():
            chatroom = chatroom[0]
            print(chatroom)
            if len(cur.fetchall()) == 1 or count == len(cur.fetchall()):
                list_message = list_message + chatroom 
            else:
                list_message = chatroom + "," + list_message
            count = count + 1
        
        if count == 0:
            return "There are no rooms yet \n Try Creating a room using the 'create' command"
        
        else:
            return "Here is a list of all current chatrooms:" + list_message

def namesof(input):
    if input[0] == 'namesof':
        chatroom = input[2] 
        cur = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])
        list_message = ""
        count = 0
        for chatroom in cur.fetchall():
            chatroom = chatroom[0]
            print(chatroom)
            if len(cur.fetchall()) == 1 or count == len(cur.fetchall()):
                list_message = list_message + chatroom 
            else:
                list_message = chatroom + "," + list_message
            count = count + 1
            
        return "Here is a list of all current users of", chatroom + list_message

    return None

def leave(input):
    if input[0] == 'leave':
        chatroom = "N/A"
        db.execute('UPDATE names SET chat_name = ? WHERE username = ?', [chatroom, str(input[1])])
        db.commit()

def close(input):
    if input[0] == 'close':
        return 'leave'
    return 'stay'

def file(input):
    if input[0] == 'file':
        print("hi")



class ChatRoom(socketserver.StreamRequestHandler):

    print("Do we get to ChatRoom?")
    def handle(self):

        print("hi?")
            
        
        #we can tell if we got connected from here
        client = f'{self.client_address} on {threading.currentThread().name}'
        print(f'Connected: {client}')
    
        while True:

            print("I'm in the True Statement")
            #data = s.recv(1024)
            # need to find someway to get the right number of bytes to read, which is in the message itself
            digits = ["0","1","2","3","4","5","6","7","8","9"]
            char = self.rfile.read(1)
            char = char.decode("utf-8")
            print("this is the first first digit:", char)
            size = True
            while size == True:
                new_char = self.rfile.read(1)
                print("Here is my new_char:", new_char)
                new_char = new_char.decode("utf-8")
                if new_char in digits:
                    char = char + new_char
                    print("The new string of digits is:", char)
                else:
                    size = False
            
            command_size = int(char) - 1
            #self.wfile.write(str(command_size).encode("utf-8"))
            print(command_size)
            new_data = self.rfile.read(command_size)
            

            data = new_data.decode("utf-8")
            data_list = data.split()
            print("Here is the data_list at this time", data_list)

            #data_list = data.split()
            #while int(size + 1) == True:
               # size = int(self.rfile.read(1)) + size

            #size = int(size.decode("utf-8"))
            #print("This is the size of the file:", size)
            #data = self.rfile.read(size)
    
            #print("Here is my data undecoded", data)
            #data = data.decode("utf-8")
            
            print("Here is my data:", data)
            
            
            if not data or data == '\n':
                break

            
            #data_list = data.split()
            print(data_list)

            lock, name = set_username(data_list)

            if name != None:
                Dict.update({name : [self.wfile, lock]})
                message_length = len('Welcome '+ name)
                message_length = str(message_length)
                self.wfile.write(message_length.encode("utf-8"))
                self.wfile.write(('Welcome '+ name).encode('utf-8'))
                print(Dict)
            
            list_message = names(data_list)

            if list_message != None:
                print("list_message = ", list_message)
                self.wfile.write(str(len(list_message) + 1).encode('utf-8'))
                self.wfile.write(list_message.encode('utf-8'))
            
            
            #if data_list[1] == 'set_username':
            #    lock, name = set_username(data_list)
            #    Dict.update({name : [self.wfile, lock]})
            #    self.wfile.write(('Welcome '+ name).encode('utf-8'))
            #    print(Dict)

            #elif data_list[1] == 'names':   
                # print out a list of all of the names
            #   list_message = names()
            #   self.wfile.write(list_message.encode('utf-8'))

            
            message(data_list)
                
            create(data_list)

            available = join(data_list)
            if available == False:
                self.wfile.write("Sorry this room doesn't exist".encode('utf-8'))

            list_message = rooms(data_list)
            if list_message != None:
                self.wfile.write(str(len(list_message) + 1).encode('utf-8'))
                self.wfile.write(list_message.encode('utf-8'))

            names_of_room = namesof(data_list)
            if names_of_room != None:
                self.wfile.write(str(len(names_of_room)).encode('utf-8'))
                self.wfile.write(names_of_room.encode('utf-8'))

            leave(data_list)
                
            door = close(data_list)
            if door == 'leave':
                print(f'Closed: {client}')
                self.wfile.write(("Your connection was closed \n WARNING any regular commands will now throw an error").encode('utf-8'))
                break

            if data_list[0] == 'file':
                name = data_list[2]
                print("Here is the user's name:", name)
                select_room = db.execute('SELECT chat_name from names WHERE username = ?', [name])
                #print("Here is the room", name, "is in:", select_room.fetchall())
                
                for chatroom in select_room.fetchall():
                    chatroom = chatroom[0]
                
                chatroom = str(chatroom)
                print(str(chatroom))
                
                select_users = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])

                for user in select_users.fetchall():
                    user = user[0]
                    print("User:", user)
                    
                    user_lock = Dict[user][1]
                    
                    with user_lock:
                        user_message = ""
                        
                        for x in range(len(data_list)):
                            if x >= 3:
                                user_message = user_message + " " + data_list[x]
                        
                        print("This is the sent image:", user_message)
                        Dict[user][0].write(str(len(data_list)).encode('utf-8'))
                        Dict[user][0].write((name + ":").encode('utf-8'))
                        Dict[user][0].write(user_message)
                        print("Sent message = ", user_message)

                
                        
with ThreadedTCPServer(('', 59898), ChatRoom) as server:
    print(f'The chatroom server is running...')
    #NewUser = ChatRoom(socketserver.StreamRequestHandler)
    #ChatRoom.start(NewUser)
    server.serve_forever()        


