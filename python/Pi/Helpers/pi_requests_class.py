import requests


class PiRequests:
    def __init__(self, url, params, type):
        self.url = url
        self.params = params
        self.type = type
        self.response = None

    def get_params(self):
        return self.params

    def set_params(self, params):
        self.params = params

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def set_response(self, response):
        self.response = response

    def get_response(self):
        return self.response

    def make_request(self):
        PARAMS = self.params
        type = self.type
        r = None
        if type == 'get_temp':
            r = requests.get(self.url, params=PARAMS)
        elif type == 'get_temps':
            r = requests.get(self.url, params=PARAMS)
        elif type == 'insert_temp':
            r = requests.post(self.url, params=PARAMS)
        elif type == 'update_temp':
            r = requests.put(self.url, params=PARAMS)
        elif type == 'delete_temp':
            r = requests.delete(self.url, params=PARAMS)
        elif type == 'delete_temps':
            r = requests.delete(self.url, params=PARAMS)
        elif type == 'get_users':
            r = requests.get(self.url, params=PARAMS)
        elif type == 'insert_user':
            r = requests.post(self.url, params=PARAMS)
        elif type == 'get_HID':
            r = requests.get(self.url, params=PARAMS)
        elif type == 'delete_user':
            r = requests.delete(self.url, params=PARAMS)
        return r
