#class clientclass:
def set_username(user_name):
    user_name = "  set_username  " + user_name
    user_name = str(len(user_name)) + ' ' + user_name
    return user_name.encode('utf-8')

def names():
    return "7  names".encode('utf-8')

def help():
    return """Current commands available:
    set_name: sets username
    names: returns list of all users
    close: closes connection
    help: lists all commands"""

def message(message):
    message = "  message  " + message
    message = str(len(message)) + ' ' + message
    return message.encode('utf-8')

def close_connection():
    return "7  close".encode('utf-8')