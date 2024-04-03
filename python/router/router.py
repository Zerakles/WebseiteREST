import json
import socket

from datetime import datetime
from typing import List

from fastapi import Response, FastAPI

from python.RestAPI.Helpers.requestThread import APIRequest
from python.SQLite.database import Database

db = Database()
app = FastAPI()
hostname = socket.gethostname()
if 'mmbbs' in hostname:
    hostname = 'mmbbs.local'
ip_address = socket.gethostbyname(hostname)
ip_splits = ip_address.split('.')
if ip_splits[0] == '127':
    ip_address = input('Bitte gib die letzte IP Adresse des Servers ein:')


def make_request(request: APIRequest):
    db.add_to_queue(request)
    while request.get_response() is None:
        pass
    response = request.get_response()
    request.kill_request()
    return Response(content=json.dumps(response, ensure_ascii=False), media_type="application/json")


# Temperatures routes

@app.get('/api/v1/temps/{temp_id}', )
async def get_temp(temp_id: int, HID: str):
    request = APIRequest(f'http://{ip_address}:8000/temps', {'id': temp_id, 'HID': HID}, 'get_temp')
    response = make_request(request)
    return response


@app.get('/api/v1/temps/', )
async def get_temps(HID: str, offset: int = None, limit: int = None):
    request = APIRequest(f'http://{ip_address}:8000/temps', {'HID': HID, 'offset': offset, 'limit': limit},
                         'get_temps')
    response = make_request(request)
    return response


@app.post('/api/v1/temps/', )
async def create_temp(time: datetime, temp_c: float, temp_f: float, HID: str):
    request = APIRequest(f'http://{ip_address}:8000/temps',
                         {'time': time, 'temp_c': temp_c, 'temp_f': temp_f, 'HID': HID}, 'create_temp')
    response = make_request(request)
    return response


@app.put('/api/v1/temps/{temp_id}', )
async def update_temp(temp_id: int, HID: str, temp_c: float = None, temp_f: float = None):
    request = APIRequest(f'http://{ip_address}:8000/temps',
                         {'id': temp_id, 'HID': HID, 'temp_c': temp_c, 'temp_f': temp_f}, 'update_temp')
    response = make_request(request)
    return response


@app.delete('/api/v1/temps/{temp_id}', )
async def delete_temp(temp_id: int, HID: str):
    request = APIRequest(f'http://{ip_address}:8000/temps', {'id': temp_id, 'HID': HID}, 'delete_temp')
    response = make_request(request)
    return response


@app.delete('/api/v1/temps/', )
async def delete_temps(temp_ids: List[str], HID: str):
    request = APIRequest(f'http://{ip_address}:8000/temps', {'temp_ids': temp_ids, 'HID': HID}, 'delete_temps')
    response = make_request(request)
    return response


# Users routes

@app.get('/api/v1/users/{username}', )
async def get_user(username: str, password: str):
    request = APIRequest(f'http://{ip_address}:8000/users', {'username': username, 'password': password},
                         'get_user')
    response = make_request(request)
    return response


@app.get('/api/v1/users/')
async def get_users(HID: str):
    request = APIRequest(f'http://{ip_address}:8000/users', {'HID': HID},
                         'get_users')

    response = make_request(request)
    return response


@app.post('/api/v1/users/')
async def create_user(username: str, password: str, token: str):
    request = APIRequest(f'http://{ip_address}:8000/users',
                         {'name': username, 'password': password, 'token': token}, 'create_user')
    response = make_request(request)
    return response


@app.get('/api/v1/users/HID/{username}')
async def get_HID(username: str, password: str):
    request = APIRequest(f'http://{ip_address}:8000/users', {'username': username, 'password': password},
                         'get_HID')
    response = make_request(request)
    return response


@app.delete('/api/v1/users/', )
async def delete_user(user_to_delete: dict[str, str], user_deleting: dict[str, str]):
    request = APIRequest(f'http://{ip_address}:8000/users',
                         {'user_to_delete': user_to_delete, 'user_deleting': user_deleting},
                         'delete_user')
    response = make_request(request)
    return response
