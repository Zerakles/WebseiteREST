import requests
from requests_cache import CachedSession


class PiRequests:
    response = None
    auth = None
    users_session = CachedSession(
        cache_name='cache/auth_cache', expire_after=28800)

    def __init__(self, host, username, password, token):
        self.host = host
        self.make_request({'username': username, 'password': password}, 'get_user')
        response_keys = list(self.response.keys())
        if 'message' in response_keys and str(self.response['message']) == 'User not found':
            self.users_session.cache.clear()
            self.make_request({'username': username, 'password': password, 'token': token}, 'create_user')
            self.make_request({'username': username, 'password': password}, 'get_user')
        self.auth = self.response['HID']

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
        config = {
            'get_temp': {
                'url': f'http://{self.host}:8000/api/v1/temps/{request_parameter["temp_id"]}' if request_type ==
                                                                                                 'get_temp' else None,
                'params': {
                    'temp_id': request_parameter['temp_id'],
                    'HID': self.auth
                } if request_type == 'get_temp' else None,
                'method': 'get'
            },
            'get_temps': {
                'url': f'http://{self.host}:8000/api/v1/temps/' if request_type == 'get_temps' else None,
                'params': {
                    'HID': self.auth,
                    'limit': request_parameter['limit'] if 'limit' in request_parameter else None,
                    'offset': request_parameter['offset'] if 'offset' in request_parameter else None
                } if request_type == 'get_temps' else None,
                'method': 'get'
            },
            'create_temp': {
                'url': f'http://{self.host}:8000/api/v1/temps/' if request_type == 'create_temp' else None,
                'params': {
                    'time': request_parameter['time'],
                    'temp_c': request_parameter['temp_c'],
                    'temp_f': request_parameter['temp_f'],
                    'HID': self.auth
                } if request_type == 'create_temp' else None,
                'method': 'post'
            },
            'update_temp': {
                'url': f'http://{self.host}:8000/api/v1/temps/{request_parameter["temp_id"]}' if request_type == 'update_temp' else None,
                'params': {
                    'temp_id': request_parameter['temp_id'],
                    'HID': self.auth,
                    'temp_c': request_parameter['temp_c'],
                    'temp_f': request_parameter['temp_f']
                } if request_type == 'update_temp' else None,
                'method': 'put'
            },
            'delete_temp': {
                'url': f'http://{self.host}:8000/api/v1/temps/{request_parameter["temp_id"]}' if request_type == 'delete_temp' else None,
                'params': {
                    'temp_id': request_parameter['temp_id'],
                    'HID': self.auth
                } if request_type == 'delete_temp' else None,
                'method': 'delete'
            },
            'delete_temps': {
                'url': f'http://{self.host}:8000/api/v1/temps/' if request_type == 'delete_temps' else None,
                'params': {
                    'temp_ids': request_parameter['temp_ids'],
                    'HID': self.auth
                } if request_type == 'delete_temps' else None,
                'method': 'delete'
            },
            'get_user': {
                'url': f'http://{self.host}:8000/api/v1/users/{request_parameter["username"]}' if request_type ==
                                                                                                  'get_user' else None,
                'params': {
                    'username': request_parameter['username'],
                    'password': request_parameter['password']
                } if request_type == 'get_user' else None,
                'method': 'get'
            },
            'get_users': {
                'url': f'http://{self.host}:8000/api/v1/users/' if request_type == 'get_users' else None,
                'params': {
                    'username': request_parameter['username'],
                    'password': request_parameter['password']
                } if request_type == 'get_users' else None,
                'method': 'get'
            },
            'create_user': {
                'url': f'http://{self.host}:8000/api/v1/users/' if request_type == 'create_user' else None,
                'params': {
                    'username': request_parameter['username'],
                    'password': request_parameter['password'],
                    'token': request_parameter['token']
                } if request_type == 'create_user' else None,
                'method': 'post'
            },
            'get_HID': {
                'url': f'http://{self.host}:8000/api/v1/users/HID/{request_parameter["username"]}' if request_type ==
                                                                                                      'get_HID' else
                None,
                'params': {
                    'username': request_parameter['username'],
                    'password': request_parameter['password']
                } if request_type == 'get_HID' else None,
                'method': 'get'
            },
            'delete_user': {
                'url': f'http://{self.host}:8000/api/v1/users/' if request_type == 'delete_user' else None,
                'params': {
                    'user_to_delete': request_parameter['user_to_delete'],
                    'user_deleting': request_parameter['user_deleting']
                } if request_type == 'delete_user' else None,
                'method': 'delete'
            }
        }
        if request_type in config:
            r = requests.request(config[request_type]['method'], config[request_type]['url'],
                                 params=config[request_type]['params'])
            self.set_response(r.json())
            return
