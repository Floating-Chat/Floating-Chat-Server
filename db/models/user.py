from db.database import conn


class User:
    def __init__(self, user_id: int, name: str, color: str):
        self.__id = user_id
        self.name = name
        self.color = color

    @property
    def id(self):
        return self.__id

    def serialize(self, with_id=False):
        serialized_user = {
            'name': self.name,
            'color': self.color
        }
        if with_id:
            serialized_user['id'] = self.id
        return serialized_user

    def update(self, name: str = None, color: int = None):
        query = []
        query_values = []
        if name is not None:
            query.append('name = ?')
            query_values.append(name)
            self.name = name
        if color is not None:
            query.append('color = ?')
            query_values.append(name)
            self.color = color
        query_values.append(self.id)
        query_string = ', '.join(query)
        c = conn.cursor()
        c.execute(f'UPDATE Users SET {query_string} WHERE id = ?', query_values)
        conn.commit()
        c.close()

    @classmethod
    def create(cls, name: str, color: str = "#FFF"):
        c = conn.cursor()
        c.execute('SELECT * from Users WHERE user_name = ?', (name,))
        existing_user = c.fetchone()
        if existing_user:
            c.close()
            return False
        c.execute('INSERT INTO Users (user_name, color) values(?, ?)', (name, color,))
        user_id = c.lastrowid
        conn.commit()
        c.close()
        return cls(user_id, name, color)

    @classmethod
    def get(cls, user_id: int):
        c = conn.cursor()
        c.execute('SELECT * from Users WHERE id = ?', (user_id,))
        existing_user = c.fetchone()
        c.close()
        if existing_user:
            return cls(*existing_user)
        return None

    @classmethod
    def get_by_name(cls, user_name: int):
        c = conn.cursor()
        c.execute('SELECT * from Users WHERE user_name = ?', (user_name,))
        existing_user = c.fetchone()
        c.close()
        if existing_user:
            return cls(*existing_user)
        return None

