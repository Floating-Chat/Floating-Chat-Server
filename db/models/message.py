from db.database import conn
from utils import get_current_time_millis
from db.models.user import User


class Message:
    def __init__(self, message_id: int, user: 'User', content: str, time: int):
        self.__id = message_id
        self.user = user
        self.content = content
        self.time = time

    @property
    def id(self):
        return self.__id

    def serialize(self):
        serialized_user = self.user.serialize()
        return {
            'id': self.id,
            'user': serialized_user,
            'content': self.content,
            'time': int(self.time)
        }

    @classmethod
    def create(cls, user: 'User', content: str):
        now = get_current_time_millis()
        c = conn.cursor()
        c.execute('INSERT INTO Messages (user_id, content, date_time) values(?, ?, ?)',
                  (user.id, content, str(now)))
        message_id = c.lastrowid
        conn.commit()
        c.close()
        return cls(message_id, user, content, now)

    @classmethod
    def get(cls, message_id: int):
        c = conn.cursor()
        c.execute('SELECT * from Messages WHERE id = ?', (message_id,))
        existing_message = c.fetchone()
        c.close()
        if existing_message:
            _, user_id, content, date_time = existing_message
            user = User.get(user_id)
            return cls(message_id, user, content, date_time)
        return None
