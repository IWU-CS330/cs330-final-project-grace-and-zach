import socket
import sqlite3
import socketserver
import threading

import socketserver
import threading


# make a global object to store all of the queues

#Some of this code about socket programming comes from https://realpython.com/python-sockets/#echo-client-and-server

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

with open('names.sql', 'r') as schema:
            script = schema.read()
db = sqlite3.connect('names.db', check_same_thread=False)
cur = db.cursor()
cur.executescript(script)
db.commit()

Dict = {}

class ChatRoom(socketserver.StreamRequestHandler):
    

    print("Do we get to ChatRoom?")
    def handle(self):
        print("hi?")
        
        #HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        #HOST  = "0.0.0.0" #Listen to all interfaces
        #PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        # use port 59898 for testing

        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
            # these next 6 lines of code came from   
            # https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python
            # they were used to intialize,create, and read the database

            #we can tell if we got connected from here
        client = f'{self.client_address} on {threading.currentThread().name}'
        print(f'Connected: {client}')
      

        #s.bind((HOST, PORT))
        #s.listen()
        #while True:
        #conn, addr = s.accept()
        #conn is another socket object for new incoming connection
        # addr is client address
        #with conn:
            #print(f"Connected by {addr}")
        
        while True:
            
            print("I'm in the True Statement")
            #data = conn.recv(1024)
            #data = data.decode("utf-8")
            
            #print("Here is My Data:", self.rfile.readline())
            data = self.rfile.readline()
            #self.rfile.readline()
            print("Here is my data undecoded", data)
            data = data.decode("utf-8")
            print("Here is my data:", data)
            
            
            if not data or data == '\n':
                break

            
            data_list = data.split()
            print(data_list)
            

            

            if data_list[1] == 'set_username':
                # put name in names table
                name = str(data_list[2])
                db.execute('INSERT INTO names (username, chat_name) VALUES (?,?)', [name, "N/A"])
                db.commit()
                Dict.update({name : self.wfile})
                self.wfile.write(('Welcome '+ name).encode('utf-8'))
                print(Dict)
            
            
            elif data_list[1] == 'names':   
                # print out a list of all of the names
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
                self.wfile.write(list_message.encode('utf-8'))

            elif data_list[1] == 'message':
                name = data_list[2]
                print("Here is the user's name:", name)
                select_room = db.execute('SELECT chat_name from names WHERE username = ?', [name])
                print("Here is the room", name, "is in:", select_room.fetchall())
                
                for chatroom in select_room.fetchall():
                    chatroom = chatroom[0]
                
                cur = db.execute('SELECT username from names WHERE chat_name = ?', [chatroom])
                print("Here is a list of all users in room:", chatroom, cur.fetchall())
                
                for user in cur.fetchall():
                    user = user[0]
                    print("cat")
                    print("User:", user)


                #cur = db.execute('SELECT username from names WHERE chat_name = ?', [select_room])
                #self.wfile.write(data_list[3].encode('utf-8'))
                #self.socket.sendall(data_list[2].encode('utf-8'))
                #print("hi")

            elif data_list[1] == 'create':
                chatroom = str(data_list[3])
                db.execute('INSERT INTO chatrooms (chat_name) VALUES (?)', [chatroom])
                db.commit()


            elif data_list[1] == 'join':
                 chatroom = str(data_list[3])
                 db.execute('UPDATE names SET chat_name = ? WHERE username = ?', [chatroom, str(data_list[2])])
                 db.commit()
                 
            
            elif data_list[1] == 'rooms':
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
                    self.wfile.write(("There are no rooms yet \n Try Creating a room using the 'create' command").encode('utf-8'))
                self.wfile.write(("Here is a list of all current chatrooms:" + list_message).encode('utf-8'))
            
            elif data_list[1] == 'leave':
                chatroom = "N/A"
                db.execute('UPDATE names SET chat_name = ? WHERE username = ?', [chatroom, str(data_list[2])])
                db.commit()
                


            elif data_list[1] == 'close':
                print(f'Closed: {client}')
                self.wfile.write(("Your connection was closed \n WARNING any regular commands will now throw an error").encode('utf-8'))
                break
                
with ThreadedTCPServer(('', 59898), ChatRoom) as server:
    print(f'The chatroom server is running...')
    #NewUser = ChatRoom(socketserver.StreamRequestHandler)
    #ChatRoom.start(NewUser)
    server.serve_forever()        


