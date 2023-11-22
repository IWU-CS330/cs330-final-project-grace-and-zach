#class clientclass:
#def find_command(input, message, username):


def set_username(user_name):
    user_name = "  set_username  " + user_name
    user_name = str(len(user_name)) + user_name
    return user_name.encode('utf-8')

def list_names():
    return "7  names".encode('utf-8')

def help():
    return """Current commands available:
    set_name: sets username
    names: returns list of all users
    close: closes connection
    help: lists all commands"""

def message(message, username):
    message = "  message  " + username + ": " + message
    message = str(len(message)) + message
    return message.encode('utf-8')

def create_room(room_name, username):
    message = "  create  " + room_name + ' ' + username
    message = str(len(message)) + message
    return message.encode('utf-8')

def add_user(message, username):
    message = "  add  " + username + message
    message = str(len(message)) + message
    return message.encode('utf-8')

def leave_room(username):
    message = "  leave  " + username
    message = str(len(message)) + message
    return message.encode('utf-8')

def join_room(message, username):
    message = "  join  " + username + ' ' + message
    message = str(len(message)) + message
    return message.encode('utf-8')

def list_rooms():
    return "7  rooms".encode('utf-8')

def close_connection():
    return "7  close".encode('utf-8')