import threading
from datetime import datetime
from WebseiteREST.python.SQLite.database import Database
from typing import Union


class APIRequest:
    def __init__(self, url, params, type):
        self.url = url
        self.params = params
        self.type = type
        self.response = None

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
        self.response = None
        self = None


class RequestThread(threading.Thread):
    current_request: Union[APIRequest, None] = None
    db: Database = None

    def __init__(self, db: Database = None):
        threading.Thread.__init__(self)
        self.db = db
    def set_current_request(self, request: Union[APIRequest, None] = None):
        if request is None:
            self.current_request = None
        else:
            self.current_request = request

    def process_request(self):
        PARAMS = self.current_request.get_params()
        type = self.current_request.get_type()
        self.db.crud.connect_to_db()
        r = None
        if type == 'get_temp':
            r = self.db.crud.get_temp(PARAMS['id'], PARAMS['HID'])
        elif type == 'get_temps':
            r = self.db.crud.get_temps(PARAMS['HID'], PARAMS['offset'], PARAMS['limit'])
        elif type == 'insert_temp':
            r = self.db.crud.insert_temp(PARAMS)
        elif type == 'update_temp':
            r = self.db.crud.update_temp(PARAMS['id'], PARAMS['HID'], PARAMS['temp_c'], PARAMS['temp_f'])
        elif type == 'delete_temp':
            r = self.db.crud.delete_temp(PARAMS['id'], PARAMS['HID'])
        elif type == 'delete_temps':
            r = self.db.crud.delete_temps(PARAMS['temp_ids'], PARAMS['HID'])
        elif type == 'get_users':
            r = self.db.crud.get_users(PARAMS['username'], PARAMS['password'])
        elif type == 'insert_user':
            r = self.db.crud.insert_user(PARAMS)
        elif type == 'get_HID':
            r = self.db.crud.get_HID(PARAMS['username'], PARAMS['password'])
        elif type == 'delete_user':
            r = self.db.crud.delete_user(PARAMS['username'], PARAMS['password'])
        self.current_request.set_response(r)
        self.db.crud.close_connection()
        self.set_current_request()

    def run(self):
        while True:
            if self.current_request is None:
                if self.db is not None:
                    if len(self.db.request_queue) > 0:
                        self.current_request = self.db.get_request_queue()
                        self.process_request()
                else:
                    pass
