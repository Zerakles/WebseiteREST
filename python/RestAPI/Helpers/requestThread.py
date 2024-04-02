from datetime import datetime
from typing import Union
import threading

from python.SQLite.database import Database
from python.Types.requestTypes import GetTemperature, GetTemperatures, CreateTemperature, GetUser, UpdateTemperature, \
    DeleteTemperature, DeleteTemperatures, GetHID, CreateUser, GetUsers, DeleteUser

class APIRequest:
    def __init__(self, url, params, type):
        self.url = url
        self.params = params
        self.type = type
        self.response = None
        self.date = datetime.now().timestamp()

    def get_params(self):
        return self.params

    def get_url(self):
        return self.url

    def get_type(self):
        return self.type

    def set_response(self, response):
        self.response = response

    def get_response(self):
        return self.response

    def kill_request(self):
        self.response = {'message': 'Too many requests'}
        return


class RequestThread(threading.Thread):
    current_request: Union[APIRequest, None] = None
    db: Database = None

    def __init__(self, db: Database = None):
        super().__init__()
        self.db = db

    def set_current_request(self, request: Union[APIRequest, None] = None,):
        if request is None:
            self.current_request = None
        else:
            self.current_request = request

    def process_request(self):
        if self.current_request is None:
            self.set_current_request()
        request_time = self.current_request.date
        current_time = datetime.now().timestamp()
        if current_time - request_time > 5:
            self.current_request.kill_request()
            self.set_current_request()
            return
        request_type = self.current_request.get_type()
        self.db.connect_to_db()
        r = None
        if request_type == 'get_temp':
            get_temp_params = GetTemperature(**self.current_request.get_params())
            r = self.db.get_temp(get_temp_params.id, get_temp_params.HID)
        elif request_type == 'get_temps':
            get_temps_params = GetTemperatures(**self.current_request.get_params())
            r = self.db.get_temps(get_temps_params.HID, get_temps_params.offset, get_temps_params.limit)
        elif request_type == 'create_temp':
            create_temp_params = CreateTemperature(**self.current_request.get_params())
            r = self.db.create_temp({
                'time': create_temp_params.time,
                'temp_c': create_temp_params.temp_c,
                'temp_f': create_temp_params.temp_f,
                'HID': create_temp_params.HID
            })
        elif request_type == 'update_temp':
            PARAMS = self.current_request.get_params()
            update_temp_params = UpdateTemperature(id=PARAMS['temp_id'], HID=PARAMS['HID'], temp_c=PARAMS['temp_c'] if 'temp_c' in PARAMS else None, temp_f=PARAMS['temp_f'] if 'temp_f' in PARAMS else None)
            r = self.db.update_temp(update_temp_params.id, update_temp_params.HID, update_temp_params.temp_c, update_temp_params.temp_f)
        elif request_type == 'delete_temp':
            delete_temp_params = DeleteTemperature(**self.current_request.get_params())
            r = self.db.delete_temp(delete_temp_params.id, delete_temp_params.HID)
        elif request_type == 'delete_temps':
            delete_temps_params = DeleteTemperatures(**self.current_request.get_params())
            r = self.db.delete_temps(delete_temps_params.temp_ids, delete_temps_params.HID)
        elif request_type == 'get_user':
            get_user_params = GetUser(**self.current_request.get_params())
            r = self.db.get_user(get_user_params.username, get_user_params.password)
        elif request_type == 'get_users':
            get_users_params = GetUsers(**self.current_request.get_params())
            r = self.db.get_users(get_users_params.HID)
        elif request_type == 'create_user':
            create_user_params = CreateUser(**self.current_request.get_params())
            r = self.db.create_user({
                'username': create_user_params.username,
                'password': create_user_params.password
            })
        elif request_type == 'get_HID':
            get_HID_params = GetHID(**self.current_request.get_params())
            r = self.db.get_HID(get_HID_params.username, get_HID_params.password)
        elif request_type == 'delete_user':
            delete_user_params = DeleteUser(**self.current_request.get_params())
            r = self.db.delete_user(delete_user_params.user_to_delete, delete_user_params.user_deleting)
        self.current_request.set_response(r)
        self.db.close_connection()
        self.set_current_request()

    def run(self):
        while True:
            if self.current_request is None:
                if self.db is not None:
                    if len(self.db.request_queue) > 0:
                        self.current_request = self.db.get_request_queue()
                        self.process_request()
                else:
                    continue
