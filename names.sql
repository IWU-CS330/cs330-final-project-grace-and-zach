drop table if exists names;
drop table if exists chatrooms;

CREATE TABLE names (
    name_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT
    chat_name TEXT
);

CREATE TABLE chatrooms (
    chatroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_name TEXT
);
