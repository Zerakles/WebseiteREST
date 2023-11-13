from WebseiteREST.python.RestAPI.Helpers.CRUD import RESTCRUD


class Database(RESTCRUD):
    crud = RESTCRUD()
    request_queue = []

    def __init__(self):#
        self.crud.connect_to_db()
        self.crud.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if self.crud.cursor.fetchone() is None:
            self.create_users_table()
            print("Created users table")
        else:
            print("users table exists")
        self.crud.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='temperatures'")
        if self.crud.cursor.fetchone() is None:
            self.create_temperatures_table()
            print("Created temperatures table")
        else:
            print("temperatures table exists")
        self.crud.close_connection()


    def create_users_table(self):
        self.crud.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        HID TEXT NOT NULL,
        token TEXT,
        unique(username, password, HID)
        )"""
        )
        self.crud.conn.commit()

    def add_to_queue(self, request):
        self.request_queue.append(request)

    def get_request_queue(self):
        if len(self.request_queue) == 0:
            return None
        return self.request_queue.pop(0)

    def create_temperatures_table(self):
        self.crud.cursor.execute(
            """CREATE TABLE IF NOT EXISTS temperatures (
        id INTEGER PRIMARY KEY,
        time TEXT NOT NULL,
        temp_c REAL,
        temp_f REAL,
        HID TEXT NOT NULL,
        unique(id, HID)
        )"""
        )
        self.crud.conn.commit()
