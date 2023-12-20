import json

import fastapi
import uvicorn
import socket

from WebseiteREST.python.RestAPI.Helpers.requestThread import APIRequest, RequestThread
from WebseiteREST.python.SQLite.database import Database
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()
db = Database()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://172.20.182.250",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

def make_request(request: APIRequest):
    db.add_to_queue(request)
    while request.get_response() is None:
        pass
    response = request.get_response()
    request.kill_request()
    return json.dumps(response, ensure_ascii=False)

@app.get('/')
def hello_world():
    return {'message': 'Hello, World!'}


@app.get('/api/v1/temps/{temp_id}')
def get_temp(temp_id: int, HID: str):
    request = APIRequest('http://localhost:8000/api/v1/temps', {'id': temp_id, 'HID': HID}, 'get_temp')
    return make_request(request)

@app.get('/api/v1/temps')
def get_temps(HID: str,offset: int = None, limit: int = None):
    request = APIRequest('http://localhost:8000/api/v1/temps', {'HID': HID, 'offset': offset, 'limit': limit}, 'get_temps')
    return make_request(request)

@app.post('/api/v1/temps')
def create_temp(time: str, temp_c: float, temp_f: float, HID: str):
    #time = datetime.now().strftime("%Y-%m-%dT%HH:%M:%S")
    request = APIRequest('http://localhost:8000/api/v1/temps', {'time': time, 'temp_c': temp_c, 'temp_f': temp_f, 'HID': HID}, 'create_temp')
    return make_request(request)
@app.put('/api/v1/temps/{temp_id}')
def update_temp(temp_id: int, HID: str, temp_c: float = None, temp_f: float = None):
    request = APIRequest('http://localhost:8000/api/v1/temps', {'id': temp_id, 'HID': HID, 'temp_c': temp_c, 'temp_f': temp_f}, 'update_temp')
    return make_request(request)

@app.delete('/api/v1/temps/{temp_id}')
def delete_temp(temp_id: int, HID: str):
    request = APIRequest('http://localhost:8000/api/v1/temps', {'id': temp_id, 'HID': HID}, 'delete_temp')
    return make_request(request)

@app.delete('/api/v1/temps')
def delete_temps(temp_ids, HID: str):
    request = APIRequest('http://localhost:8000/api/v1/temps', {'temp_ids': temp_ids, 'HID': HID}, 'delete_temps')
    return make_request(request)

@app.get('/api/v1/users/{username}_get')
def get_user(username: str, password: str):
    request = APIRequest('http://localhost:8000/api/v1/users', {'username': username, 'password': password}, 'get_user')
    return make_request(request)
@app.get('/api/v1/users')
def get_users(username: str, password: str):
    request = APIRequest('http://localhost:8000/api/v1/users', {'username': username, 'password': password}, 'get_users')
    return make_request(request)

@app.post('/api/v1/users')
def create_user(username: str, password: str, token: str):
    requests = APIRequest('http://localhost:8000/api/v1/users', {'name': username, 'password': password, 'token': token}, 'create_user')
    return make_request(requests)

@app.get('/api/v1/users/{username}')
def get_HID(username: str, password: str):
    request = APIRequest('http://localhost:8000/api/v1/users', {'username': username, 'password': password}, 'get_HID')
    return make_request(request)

@app.delete('/api/v1/users/{username}')
def delete_user(username: str, password: str):
    request = APIRequest('http://localhost:8000/api/v1/users', {'username': username, 'password': password}, 'delete_user')
    return make_request(request)


if __name__ == '__main__':
    thread = RequestThread(db)
    thread.start()
    uvicorn.run(app, host=ip_address, port=8000)
