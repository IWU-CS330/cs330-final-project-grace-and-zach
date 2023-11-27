import socket
import sqlite3
import socketserver
import threading

import socketserver
import threading




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
        first = True
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
                self.wfile.write(('Welcome '+ name).encode('utf-8'))
            
            
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
                self.wfile.write(list_message.encode('utf-8'))

            elif data_list[1] == 'message':
                self.wfile.write(data_list[2].encode('utf-8'))

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
                self.wfile.write(list_message.encode('utf-8'))
            
            elif data_list[1] == 'leave':
                chatroom = "N/A"
                db.execute('UPDATE names SET chat_name = ? WHERE username = ?', [chatroom, str(data_list[2])])
                db.commit()
                self.wfile.write("You have Left the Chatroom \n and Returned to the Main Room" + chatroom.encode("uft-8"))


            elif data_list[1] == 'close':
                print(f'Closed: {client}')
                break
                
with ThreadedTCPServer(('', 59898), ChatRoom) as server:
    print(f'The chatroom server is running...')
    #NewUser = ChatRoom(socketserver.StreamRequestHandler)
    #ChatRoom.start(NewUser)
    server.serve_forever()        


