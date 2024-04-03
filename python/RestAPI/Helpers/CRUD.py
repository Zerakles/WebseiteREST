import random
import sqlite3
import string
import numpy as np
from datetime import datetime

from pydantic import Field
from secrets import compare_digest


class RESTCRUD:
    db = None
    conn = None
    cursor = None
    df = None
    query = None
    error_message = 'Could not execute query'

    last_user_update = 0
    last_user_lookup = None
    users = np.array([])
    last_temperature_update: dict[str, float] = {}
    last_temperature_lookup: dict[str, float] = {}
    temperatures: dict[str, np.ndarray] = {}

    def __init__(self):
        self.connect_to_db()

    def set_query(self, query: str = None):
        self.query = query

    def execute_query(self):
        try:
            self.cursor.execute(self.query)
        except sqlite3.Error:
            err = sqlite3.Error
            return {'message': f'{err} \n{self.error_message}'}

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        self.db = None
        self.conn = None
        self.cursor = None
        self.query = None
        self.error_message = 'Could not execute query'

    def connect_to_db(self):
        self.conn = sqlite3.connect('SQLite/DB/PiRest.db')
        self.cursor = self.conn.cursor()

    def check_if_temp_cache_is_valid(self, HID: str):
        if self.temperatures[HID] is None:
            return False
        if self.temperatures[HID].size == 0:
            return False
        if self.last_temperature_lookup[HID] is None:
            return False
        if self.last_temperature_update[HID] is None:
            return False
        if self.last_temperature_update[HID] > self.last_temperature_lookup[HID]:
            return False
        return True

    def get_temp(self, temp_id: int, HID: str):
        if self.check_if_temp_cache_is_valid(HID):
            for temp in self.temperatures[HID]:
                if compare_digest(str(temp['id']), str(temp_id)) and compare_digest(temp['HID'], HID):
                    return {'temp_c': temp['temp_c'], 'temp_f': temp['temp_f']}
            return {'message': 'Temperature not found'}
        self.query = f"SELECT * FROM temperatures WHERE id = {temp_id} AND HID = '{HID}'"
        self.execute_query()
        fetch = self.cursor.fetchone()
        if fetch is None:
            return {'message': 'Temperature not found'}
        data = {
            'id': fetch[0],
            'time': fetch[1],
            'temp_c': fetch[2],
            'temp_f': fetch[3],
            'HID': fetch[4]
        }
        return {'temp_c': data['temp_c'], 'temp_f': data['temp_f']}

    def get_temps(self, HID: str, offset: int = 0, limit: int = None):
        if self.check_if_temp_cache_is_valid(HID):
            sorted_temps = sorted(self.temperatures[HID], key=lambda x: x['id'], reverse=True)
            if limit:
                if offset is None:
                    offset = 0
                return sorted_temps[::-1][offset:limit]
            else:
                return sorted_temps
        if offset is None:
            offset = 0
        self.query = f'SELECT * FROM temperatures WHERE HID = "{HID}" ORDER BY id DESC'
        self.execute_query()
        fetch = self.cursor.fetchall()
        all_temps = []
        if fetch is None:
            return {'message': 'No temperatures found'}
        for entry in fetch:
            all_temps.append({
                'id': entry[0],
                'time': entry[1],
                'temp_c': entry[2],
                'temp_f': entry[3],
                'HID': entry[4]
            })
        self.temperatures[HID] = np.array(all_temps)
        if limit:
            self.query += f' LIMIT {limit} OFFSET {offset}'
        self.execute_query()
        fetch = self.cursor.fetchall()
        data = []
        if fetch is None:
            return {'message': 'No temperatures found'}
        for entry in fetch:
            data.append({
                'id': entry[0],
                'time': entry[1],
                'temp_c': entry[2],
                'temp_f': entry[3],
                'HID': entry[4]
            })
        self.last_temperature_lookup[HID] = datetime.now().timestamp()
        return data

    def create_temp(self, data):
        time, temp_c, temp_f, HID = data.values()
        self.query = (f"INSERT INTO temperatures (time, temp_c, temp_f, HID) VALUES ('{time}', {temp_c}, {temp_f}, "
                      f"'{HID}')")
        self.execute_query()
        self.conn.commit()
        self.last_temperature_update[HID] = datetime.now().timestamp()
        return {'message': f'New temperature inserted'}

    def update_temp(self, temp_id: int, HID: str,
                    temp_c: float = Field(None), temp_f: float = Field(None)
                    ):
        if temp_c is not None:
            self.query = f"UPDATE temperatures SET temp_c = {temp_c} WHERE id = {temp_id} AND HID = '{HID}'"
            self.execute_query()
        if temp_f is not None:
            self.query = f"UPDATE temperatures SET temp_f = {temp_f} WHERE id = {temp_id} AND HID = '{HID}'"
            self.execute_query()
        self.conn.commit()
        self.last_temperature_update[HID] = datetime.now().timestamp()
        return {'message': f'Temperature with id: {temp_id} updated'}

    def delete_temp(self, temp_id: int, HID: str):
        self.query = f"DELETE FROM temperatures WHERE id = {temp_id} AND HID = '{HID}'"
        self.error_message = f'Temperature {temp_id} not found'
        self.execute_query()
        self.conn.commit()
        self.last_temperature_update = datetime.now().timestamp()

        return {'message': f'Temperature {temp_id} deleted'}

    def delete_temps(self, temp_ids: list[int], HID: str):
        for temp_id in temp_ids:
            self.query = f"DELETE FROM temperatures WHERE id = {temp_id} AND HID = '{HID}'"
            self.execute_query()
            self.conn.commit()
        self.last_temperature_update = datetime.now().timestamp()

        return {'message': f'Temperatures {temp_ids} deleted'}

    def get_HID(self, username: str, password: str):
        if self.users.size > 0 and self.last_user_lookup is not None:
            if self.last_user_update < self.last_user_lookup:
                for user in self.users:
                    if compare_digest(user['username'], username) and compare_digest(user['password'], password):
                        return user['HID']
                return {'message': 'User not found'}
        self.query = f"SELECT HID FROM users WHERE username = '{username}' AND password = '{password}'"
        self.execute_query()
        data = self.cursor.fetchone()
        if data is None:
            return {'message': 'User not found'}
        return data[0]

    def generate_HID(self):
        characters = string.ascii_letters + string.digits
        HID = ''.join(random.choice(characters) for _ in range(9))
        return HID

    def get_user(self, username: str, password: str):
        if self.users.size > 0 and self.last_user_lookup:
            if self.last_user_update < self.last_user_lookup:
                for user in self.users:
                    if compare_digest(user['username'], username) and compare_digest(user['password'], password):
                        return user
                return {'message': 'User not found'}

        self.query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        self.execute_query()
        fetch = self.cursor.fetchone()
        if fetch is None:
            return {'message': 'User not found'}
        data = {
            'username': fetch[0],
            'password': fetch[1],
            'HID': fetch[2],
            'token': fetch[3]
        }
        return data

    def get_users(self, HID: str):
        if not self.check_for_permission(HID):
            return 'Permission denied'
        else:
            if self.users.size > 0 and self.last_user_update is not None:
                if self.last_user_update < self.last_user_lookup:
                    return self.users.tolist()
            try:
                self.query = "SELECT * FROM users"
                self.execute_query()
                fetch = self.cursor.fetchall()
                data = []
                for entry in fetch:
                    data.append({
                        'username': entry[0],
                        'password': entry[1],
                        'HID': entry[2],
                        'token': entry[3]
                    })
                self.users = np.array(data)
                self.last_user_lookup = datetime.now().timestamp()
                return data
            except sqlite3.Error:
                err = sqlite3.Error
                return {'message': err}

    def create_user(self, data: dict):
        username, password, token = data.values()
        self.cursor.execute("SELECT HID FROM users")
        HIDS = self.cursor.fetchall()
        HID = self.generate_HID()
        while HID in HIDS:
            HID = self.generate_HID()
        try:
            self.query = (f'INSERT INTO users (username, password, HID, token) VALUES ({username}'
                          f', {password}, {f"Client_{HID}"}, {token})')
            self.execute_query()
            self.conn.commit()
            self.last_user_update = datetime.now().timestamp()
            return {'message': f'User {username} created'}
        except sqlite3.Error:
            err = sqlite3.Error
            return {'message': f'{err} \nCould not create user'}

    def check_for_permission(self, HID: str):
        self.query = f"SELECT token FROM users WHERE HID = '{HID}'"
        self.execute_query()
        self.conn.commit()
        fetch = self.cursor.fetchone()
        return fetch is not None and fetch[0] == 'admin'

    def delete_user(self, user_to_delete: dict[str, str], user_deleting: dict[str, str]):
        username, password = user_to_delete.values()
        if self.check_for_permission(user_deleting['HID']):
            self.query = f"DELETE FROM users WHERE username = '{username}' AND password = '{password}'"
            self.execute_query()
            self.conn.commit()
            self.last_user_update = datetime.now().timestamp()
            return {'message': 'User deleted'}
        return {'message': 'Permission denied'}
