import json

import requests


class PiRequests:
    response = None
    auth = None

    def __init__(self, host, username , password, token):
        self.host = host
        self.make_request({'username': username, 'password': password}, 'get_user')
        if str(self.response).replace('"', '') == 'User not found':
            self.make_request({'username': username, 'password': password, 'token': token}, 'create_user')
            self.make_request({'username': username, 'password': password}, 'get_user')
        self.auth = json.loads(self.response)

    def get_host(self):
        return self.host

    def set_host(self, host):
        self.host = host

    def set_response(self, response):
        self.response = response

    def get_response(self):
        return self.response

    def get_auth(self):
        return self.auth

    def set_auth(self, auth):
        self.auth = auth

    def make_request(self, request_parameter, request_type):
        r = None
        if request_type == 'get_temp':
            temp_params = {
                'temp_id': request_parameter['temp_id'],
                'HID': self.auth['HID']
            }
            r = requests.get(f'http://{self.host}:8000/api/v1/temps/{temp_params["temp_id"]}?temp_id={temp_params["temp_id"]}&HID={temp_params["HID"]}')
        elif request_type == 'get_temps':
            temp_params = {
                'HID': self.auth['HID'],
                'limit': request_parameter['limit'] if 'limit' in request_parameter else None,
                'offset': request_parameter['offset'] if 'offset' in request_parameter else None
            }
            if temp_params['limit'] is None and temp_params['offset'] is None:
                r = requests.get(f'http://{self.host}:8000/api/v1/temps?HID={temp_params["HID"]}')
            elif temp_params['limit'] is not None and temp_params['offset'] is None:
                r = requests.get(f'http://{self.host}:8000/api/v1/temps?HID={temp_params["HID"]}&limit={temp_params["limit"]}')
            elif temp_params['limit'] is None and temp_params['offset'] is not None:
                r = requests.get(f'http://{self.host}:8000/api/v1/temps?HID={temp_params["HID"]}&limit={temp_params["limit"]}&offset={temp_params["offset"]}')
            else: return 'Error in make_request in pi_requests_class.py in get_temps'
        elif request_type == 'create_temp':
            temp_params = {
                'time': request_parameter['time'],
                'temp_c': request_parameter['temp_c'],
                'temp_f': request_parameter['temp_f'],
                'HID': self.auth['HID']
            }
            r = requests.post(f'http://{self.host}:8000/api/v1/temps', params=temp_params)
        elif request_type == 'update_temp':
            temp_params = {
                'temp_id': request_parameter['temp_id'],
                'HID': self.auth['HID'],
                'temp_c': request_parameter['temp_c'],
                'temp_f': request_parameter['temp_f']
            }
            r = requests.put(f'http://{self.host}:8000/api/v1/temps', params=temp_params)
        elif request_type == 'delete_temp':
            temp_params = {
                'temp_id': request_parameter['temp_id'],
                'HID': self.auth['HID']
            }
            r = requests.delete(f'http://{self.host}:8000/api/v1/temps', params=temp_params)
        elif request_type == 'delete_temps':
            temp_params = {
                'temp_ids': request_parameter['temp_ids'],
                'HID': self.auth['HID']
            }
            r = requests.delete(f'http://{self.host}:8000/api/v1/temps', params=temp_params)
        elif request_type == 'get_user':
            user_request_parameter = {
                'username': request_parameter['username'],
                'password': request_parameter['password']
            }
            r = requests.get(
                f'http://{self.host}:8000/api/v1/users/{user_request_parameter["username"]}_get?username={user_request_parameter["username"]}&password={user_request_parameter["password"]}')
        elif request_type == 'get_users':
            user_request_parameter = {
                'username': request_parameter['username'],
                'password': request_parameter['password']
            }
            r = requests.get(f'http://{self.host}:8000/api/v1/users?username={user_request_parameter["username"]}&password={user_request_parameter["password"]}')
        elif request_type == 'create_user':
            user_request_parameter = {
                'username': request_parameter['username'],
                'password': request_parameter['password'],
                'token': request_parameter['token']
            }
            r = requests.post(f'http://{self.host}:8000/api/v1/users', params=user_request_parameter)
        elif request_type == 'get_HID':
            user_request_parameter = {
                'username': request_parameter['username'],
                'password': request_parameter['password']
            }
            r = requests.get(f'http://{self.host}:8000/api/v1/users/{user_request_parameter["username"]}?username={user_request_parameter["username"]}&password={user_request_parameter["password"]}', params=user_request_parameter)
        elif request_type == 'delete_user':
            user_request_parameter = {
                'username': request_parameter['username'],
                'password': request_parameter['password']
            }
            r = requests.get(
                f'http://{self.host}:8000/api/v1/users/{user_request_parameter["username"]}?username={user_request_parameter["username"]}&password={user_request_parameter["password"]}',
                params=user_request_parameter)
        self.set_response(r.json())
