import sqlite3

conn = sqlite3.connect('chat.db')


def create_tables():
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name VARCHAR(25) NOT NULL,
            color VARCHAR(9)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS Messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT,
            content TEXT NOT NULL,
            date_time TEXT NOT NULL,
            FOREIGN KEY (user_id)
            REFERENCES Users (id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)
    c.close()
    conn.commit()


create_tables()
