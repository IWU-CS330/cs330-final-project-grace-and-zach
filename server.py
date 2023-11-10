# echo-server.py

import socket
import sqlite3


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#HOST  = "0.0.0.0" #Listen to all interfaces
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

#Some of this code about socket programming comes from https://realpython.com/python-sockets/#echo-client-and-server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
    # these next 6 lines of code came from   
    # https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python
    # they were used to intialize,create, and read the database

    with open('names.sql', 'r') as schema:
        script = schema.read()
    
    db = sqlite3.connect('names.db')
    cur = db.cursor()
    cur.executescript(script)
    db.commit()

    s.bind((HOST, PORT))
    s.listen()
    #while True:
    conn, addr = s.accept()
    #conn is another socket object for new incoming connection
    # addr is client address
    with conn:
        print(f"Connected by {addr}")
    
        while True:
            data = conn.recv(1024)
            data = data.decode("utf-8")

            if not data or data == '\n':
                break

            data_list = data.split()

            if data_list[1] == 'name':
                # put name in names table
                name = str(data_list[2])
                db.execute('INSERT INTO names (username) VALUES (?)', [name])
                db.commit()
                conn.sendall(('Welcome '+ name).encode('utf-8'))
            
            
            elif data_list[1] == 'names':   
                # print out a list of all of the names
                cur = db.execute('SELECT username from names')
                for username in cur.fetchall():
                    username = username[0]
                    print(username)
                    conn.sendall(username.encode('utf-8'))
                conn.sendall('stop'.encode('utf-8'))

          