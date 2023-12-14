import socket
import sqlite3
import socketserver
import threading

import socketserver
import threading
import sys
import os


#Some of this code about socket programming comes from https://realpython.com/python-sockets/#echo-client-and-server
# Some of this code, for making a multithreaded server came from https://cs.lmu.edu/~ray/notes/pythonnetexamples/

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

# dictionary to store each user's: name, socket object, and lock object
Dict = {}

# dictionary to store each user's: name and public key
Key_Dict = {}

# Adds a new user to the data table, names and makes its lock object
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
    
# sends out a list of all of the users of the application
def names(input):
    if input[0] == 'names':
        cur = db.execute('SELECT username from names')
        list_message = ""
        count = 0
        for username in cur.fetchall():
            username = username[0]
            print(username)  
            # asks if there's only 1 name or if its the last name for readability purposes          
            if len(cur.fetchall()) == 1 or count == len(cur.fetchall()):
                list_message = list_message + username 
            else:
                list_message = username + "," + list_message
            count = count + 1
                
        list_message = "Here is a list of all current users:" + list_message
        
        return list_message  
    
    else:
        return None

# sends a message to every person within the group you are apart of 
def message(input):
    if input[0] == 'message':         
        name = input[1]
        print("Here is the user's name:", name)
        select_room = db.execute('SELECT chat_name from names WHERE username = ?', [name])
        
        for chatroom in select_room.fetchall():
            chatroom = chatroom[0]
        
        chatroom = str(chatroom)
        print(str(chatroom))
        
        select_users = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])

        for user in select_users.fetchall():
            user = user[0]
            # for testing purposes
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
                    #for testing purposes
                    print("Sent message = ", user_message)

# creates a new chatroom in the chatrooms table
def create(input):
    if input[0] == 'create':
        chatroom = str(input[2])
        db.execute('INSERT INTO chatrooms (chat_name) VALUES (?)', [chatroom])
        db.commit()

# makes you a member of your requested chatroom, updates the names table
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
        
# makes a list of all of the currently made rooms, even if the rooms are empty and sends it out to the user
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

# outputs a list of names for a particular room
def namesof(input):
    if input[0] == 'namesof':
        chatroom = input[1] 
        cur = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])
        list_message = ""
        count = 0
        for user in cur.fetchall():
            user = user[0]
            print(user)
            if len(cur.fetchall()) == 1 or count == len(cur.fetchall()):
                list_message = list_message + user
            else:
                list_message = user + "," + list_message
            count = count + 1
            
        return "Here is a list of all current users of "+ chatroom + ":" + list_message

    return None

# lets you leave a room and stop recieving messages from it
def leave(input):
    if input[0] == 'leave':
        chatroom = "N/A"
        db.execute('UPDATE names SET chat_name = ? WHERE username = ?', [chatroom, str(input[1])])
        db.commit()

# closes application all together
def close(input):
    if input[0] == 'close':
        return 'leave'
    return 'stay'

# where the file transfer method was supposed to go once it was finished
def file(input):
    if input[0] == 'file':
        print("hi")

# sets the user's public key to the one generated by the client
def set_key(input):
    if input[0] == 'set_public_key':
        Key_Dict.update({input[1] : input[2]})

# retrieves a list of public keys for a particular chatroom
def get_key(input):
    if input[0] == 'get_public_keys':
        user_name = input[1]
        cur = db.execute('SELECT chat_name from names WHERE username = ?', [user_name])
        for room in cur.fetchall():
            chatroom = room[0]
            
        cur = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])
        list_keys = ""
        count = 0
        for user in cur.fetchall():
            user = user[0]
            if count == 0:
                list_keys = "get_public_keys " + Key_Dict[user] +" " + list_keys
            else:
                list_keys = Key_Dict[user] + " " + list_keys
            count = count + 1 

        return list_keys
    
    else:
        return None



class ChatRoom(socketserver.StreamRequestHandler):
    # Checks to see if we made it into the Chatroom class
    print("Do we get to ChatRoom?")
    def handle(self):
      
            
        
        #we can tell if we got connected from here
        client = f'{self.client_address} on {threading.currentThread().name}'
        print(f'Connected: {client}')
    
        while True:

            print("I'm in the True Statement")
            # list of digits for checking the size of the message
            digits = ["0","1","2","3","4","5","6","7","8","9"]
            char = self.rfile.read(1)
            char = char.decode("utf-8")
            # for testing purposes
            print("this is the first first digit:", char)
            size = True

            # keeps reading digits one at a time, until it runs into a char that's not a digit and thus isn't apart of the size
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
            print(command_size)
            new_data = self.rfile.read(command_size)
            # splits the data given into a list, so our functions can handle it easier
            data_list = new_data.split()
            
            # not working code for file transfer
            # decodes the command word file to see if a file transfer is needed
            if data_list[0].decode("utf-8") == 'file':

                # checks for the user's name
                name = data_list[2].decode("utf-8")
                print("Here is the user's name:", name)

                #looks to see what room the user is in
                select_room = db.execute('SELECT chat_name from names WHERE username = ?', [name])
                #print("Here is the room", name, "is in:", select_room.fetchall())
                
                for chatroom in select_room.fetchall():
                    chatroom = chatroom[0]
                
                chatroom = str(chatroom)
                print(str(chatroom))
                
                # find all of the other users within the sender's chatroom
                select_users = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])

                for user in select_users.fetchall():
                    user = user[0]
                    print("User:", user)
                    
                    # get the user's lock object from the dictionary
                    user_lock = Dict[user][1]
                    
                    with user_lock:
                        user_message = []
                        print("The name of file:", data_list[1])

                        # sends the length of file + the name of the file 
                        Dict[user][0].write(str(len("file " + data_list[1].decode('utf-8'))).encode('utf-8'))
                        Dict[user][0].write(("file " + data_list[1].decode('utf-8')).encode('utf-8'))
                        
                   
                        # for every bit in the message 
                        for x in range(len(data_list)):
                          if x >= 3:
                              #with open("new_file.txt", "wb") as bin_file:
                               #   bin_file.write(data_list[x])
                              #print("DataList = ", data_list[x])
                              #if '\x00' in data_list[x]:
                               #user_message = user_message.append(" ")
                              #else:
                              # user_message = user_message.append(data_list[x])
                              #Dict[user][0].write(str(len("file " + data_list[x])).encode("utf-8"))
                              #Dict[user][0].write("file " + data_list[x])
                             # print("This is the sent image:", data_list[x])
                          #elif x > 3:

                            # send the length of the single bit
                            Dict[user][0].write((str(len(str(data_list[x])))).encode('utf-8'))
                            # send the bit itself to the client
                            Dict[user][0].write(data_list[x])

                            #  print("This is the sent image:", data_list[x])

                        #print("This is the sent image:", user_message)
                        #bin_file.close()
                        #file_size = os.stat("new_file.txt").st_size

                        #Dict[user][0].write(str(len(user_message)).encode('utf-8'))
                        #for x in range(len(user_message)):
                        #    Dict[user][0].write(user_message[x])

                        #Dict[user][0].write(str(len("file" + " " + data_list[1].decode('utf-8') + " ") + file_size).encode('utf-8'))
                        #Dict[user][0].write(("file" + " " + data_list[1].decode('utf-8') + " " + bin_file).encode('utf-8'))

                       

                        #Dict[user][0].write(str(file_size).encode('utf-8'))
                        #Dict[user][0].write(bin_file)
                        #Dict[user][0].write(str(len(user_message)).encode('utf-8'))
                        #Dict[user][0].write(user_message)
                        #print("Sent message = ", user_message)

            # decodes all of the given data  
            data = new_data.decode("utf-8")
            data_list = data.split()
            # splits the data again just to be sure

            # for testing purposes
            print("Here is the data_list at this time", data_list)

            
            print("Here is my data:", data)
            
            
            if not data or data == '\n':
                break


            # checks what is in the message after the size
            print(data_list)

            # calls each server function to see if it is needed in its particular scenerario
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
                self.wfile.write(str(len(names_of_room) + 1).encode('utf-8'))
                self.wfile.write(names_of_room.encode('utf-8'))

            key_list = get_key(data_list)
            if key_list != None:
                self.wfile.write(str(len(key_list)).encode('utf-8'))
                self.wfile.write(key_list.encode('utf-8'))

            leave(data_list)
                
            door = close(data_list)
            if door == 'leave':
                print(f'Closed: {client}')
                self.wfile.write(str(len(("Your connection was closed \n WARNING any regular commands will now throw an error"))).encode("utf-8"))
                self.wfile.write(("Your connection was closed \n WARNING any regular commands will now throw an error").encode('utf-8'))
                break

            
# starts the server to begin with                         
with ThreadedTCPServer(('', 59898), ChatRoom) as server:
    print(f'The chatroom server is running...')
    #NewUser = ChatRoom(socketserver.StreamRequestHandler)
    #ChatRoom.start(NewUser)
    server.serve_forever()        


