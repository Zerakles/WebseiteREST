from python.RestAPI.Helpers.CRUD import RESTCRUD
import os
import numpy as np


class Database(RESTCRUD):
    request_queue = np.array([])
    response_queue = np.array([])

    def __init__(self):
        super().__init__()
        # test if Folder DB exists
        if not os.path.exists('SQLite/DB'):
            os.makedirs('SQLite/DB')
        self.set_query("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        self.execute_query()
        self.set_query()
        if self.cursor.fetchone() is None:
            self.create_users_table()
            print("Created users table")
        self.set_query("SELECT name FROM sqlite_master WHERE type='table' AND name='temperatures'")
        self.execute_query()
        self.set_query()
        if self.cursor.fetchone() is None:
            self.create_temperatures_table()
            print("Created temperatures table")
        self.close_connection()

    def create_users_table(self):
        self.set_query("""CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        HID TEXT NOT NULL,
        token TEXT,
        unique(username, password, HID)
        )""")
        self.execute_query()
        self.conn.commit()

    def add_to_queue(self, request):
        if self.request_queue.size == 50:
            self.request_queue = np.delete(self.request_queue, 0)
        self.request_queue = np.append(self.request_queue, request)

    def get_request_queue(self):
        if self.request_queue.size == 0:
            return None
        request = self.request_queue[0]
        self.request_queue = np.delete(self.request_queue, 0)
        return request

    def get_response_queue(self):
        if self.response_queue.size == 0:
            return None
        response = self.response_queue[0]
        self.response_queue = np.delete(self.response_queue, 0)
        return response

    def create_temperatures_table(self):
        self.set_query("""CREATE TABLE IF NOT EXISTS temperatures (
        id INTEGER PRIMARY KEY,
        time TEXT NOT NULL,
        temp_c REAL,
        temp_f REAL,
        HID TEXT NOT NULL,
        unique(id, HID)
        )""")
        self.execute_query()
        self.conn.commit()
