import random
import sqlite3
import string

import polars as pl
from pydantic import Field


class RESTCRUD:
    db = None
    conn = None
    cursor = None
    df = None

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        self.db = None
        self.conn = None
        self.cursor = None

    def connect_to_db(self):
        self.db = 'SQLite/DB/PiRest.db'
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def get_temp(self, temp_id: int, HID: str):
        try:
            self.cursor.execute("SELECT * FROM temperatures WHERE id = ? AND HID = ?", (temp_id, HID))
            fetch = self.cursor.fetchone()
            if fetch is None:
                return 'Temperature not found'
            else:
                data = {
                    'id': fetch[0],
                    'time': fetch[1],
                    'temp_c': fetch[2],
                    'temp_f': fetch[3],
                    'HID': fetch[4]
                }
                return {'temp_c': data['temp_c'], 'temp_f': data['temp_f']}
        except sqlite3.Error:
            err = sqlite3.Error
            return f'{err} \bTemperature could not be found'

    def get_temps(self, HID: str, offset: int = 0, limit: int = None):
        try:
            if limit is None or offset is None:
                self.cursor.execute("SELECT * FROM temperatures WHERE HID = ?", (HID,))
            else:
                self.cursor.execute("SELECT * FROM temperatures WHERE HID = ? LIMIT ? OFFSET ?", (HID, limit, offset))
            fetch = self.cursor.fetchall()
            data = []
            if fetch is None:
                return 'No temperatures found'
            else:
                for entry in fetch:
                    data.append({
                        'id': entry[0],
                        'time': entry[1],
                        'temp_c': entry[2],
                        'temp_f': entry[3]
                    })
                return data
        except sqlite3.Error:
            err = sqlite3.Error
            return f'{err} \bCould not get temperatures'

    def create_temp(self, data):
        time, temp_c, temp_f, HID = data.values()
        try:
            self.cursor.execute("INSERT INTO temperatures (time, temp_c, temp_f, HID) VALUES (?, ?, ?, ?)",
                                (time, temp_c, temp_f, HID))
            self.conn.commit()
            self.cursor.execute("SELECT id FROM temperatures WHERE HID = ?", (HID,))
            data = self.cursor.fetchall()
            if data is not None:
                return f'Temperature with id: {data[-1][0]} inserted'
        except sqlite3.Error:
            err = sqlite3.Error
            return f'{err} \bCould not insert temperature'


    def update_temp(self, temp_id: int, HID: str,
                     temp_c: float = Field(None), temp_f: float = Field(None)
                     ):
        if temp_c is not None:
            try:
                self.cursor.execute("UPDATE temperatures SET temp_c = ? WHERE id = ? AND HID = ?", (temp_c, temp_id, HID))
            except sqlite3.Error:
                err = sqlite3.Error
                return f'{err} \bTemperature with id: {temp_id} not found'
        if temp_f is not None:
            try:
                self.cursor.execute("UPDATE temperatures SET temp_f = ? WHERE id = ? AND HID = ?", (temp_f, temp_id, HID))
            except sqlite3.Error:
                err = sqlite3.Error
                return f'{err} \bTemperature {temp_id} not found'
        self.conn.commit()
        return f'Temperature with id: {temp_id} updated'

    def delete_temp(self, temp_id: int, HID: str):
        try:
            self.cursor.execute("DELETE FROM temperatures WHERE id = ? AND HID = ?", (temp_id, HID))
        except sqlite3.Error:
            err = sqlite3.Error
            return f'{err} \bTemperature {temp_id} not found'
        self.conn.commit()
        return f'Temperature {temp_id} deleted'

    def delete_temps(self, temp_ids: list[int], HID: str):
        for temp_id in temp_ids:
            try:
                self.cursor.execute("DELETE FROM temperatures WHERE id = ? AND HID = ?", (temp_id, HID))
            except sqlite3.Error:
                err = sqlite3.Error
                return f'{err} \bTemperature {temp_id} not found'
        self.conn.commit()
        return f'Temperatures {temp_ids} deleted'

    def get_HID(self, username: str, password: str):
        try:
            self.cursor.execute("SELECT HID FROM users WHERE username = ? AND password = ?", (username, password))
            data = self.cursor.fetchone()
            if data is None:
                return 'User not found'
            else:
                return data[0]
        except sqlite3.Error:
            err = sqlite3.Error
            return f'{err} \bUser could not be found'

    def generate_HID(self):
        characters = string.ascii_letters + string.digits
        HID = ''.join(random.choice(characters) for _ in range(9))
        return HID

    def get_user(self, username: str, password: str):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            fetch = self.cursor.fetchone()
            if fetch is None:
                return 'User not found'
            else:
                data = {
                    'username': fetch[0],
                    'password': fetch[1],
                    'HID': fetch[2],
                    'token': fetch[3]
                }
                return data
        except sqlite3.Error:
            err = sqlite3.Error
            return f'{err} \bUser could not be found'



    def get_users(self, username: str, password: str):
        if not self.isAdmin(username,password):
            return 'Permission denied'
        else:
            try:
                self.cursor.execute("SELECT * FROM users")
                fetch = self.cursor.fetchall()
                data = []
                for entry in fetch:
                    data.append({
                        'username': entry[0],
                        'password': entry[1],
                        'HID': entry[2],
                        'token': entry[3]
                    })
                return data
            except sqlite3.Error:
                err = sqlite3.Error
                return f'{err} \bCould not get users'
    def create_user(self, data: dict):
        username, password, token = data.values()
        self.cursor.execute("SELECT HID FROM users")
        HIDS = self.cursor.fetchall()
        HID = self.generate_HID()
        while HID in HIDS:
            HID = self.generate_HID()
        try:
            self.cursor.execute("INSERT INTO users (username, password, HID, token) VALUES (?, ?, ?, ?)",
                            (username, password, f'Client_{HID}', token))
            self.conn.commit()
            return 'User inserted'
        except sqlite3.Error:
            err = sqlite3.Error
            return f'{err} \bCould not create user'

    def isAdmin(self, username: str, password: str):
        self.cursor.execute("SELECT token FROM users WHERE username = ? AND password = ?", (username, password))
        fetch = self.cursor.fetchone()
        if fetch is not None and fetch[0] == 'admin':
            return True
        else:
            return False

    def delete_user(self, username: str, password: str):
        if not self.isAdmin(username,password):
            return 'Permission denied'
        else:
            try:
                self.cursor.execute("DELETE FROM users WHERE username = ? AND password = ?", (username, password))
                self.conn.commit()
                return 'User deleted'
            except sqlite3.Error:
                err = sqlite3.Error
                return f'{err} \bCould not delete user'


    def polar_cache(self, dataFrame: pl.DataFrame):
        self.df = dataFrame
        return self.df
