import uvicorn
import numpy as np
from RestAPI.Helpers.requestThread import RequestThread
from fastapi.middleware.cors import CORSMiddleware
from router.router import db, ip_address, app

# get the first 3 octets of the ip address
same_origin_ip = '.'.join(ip_address.split('.')[:3])
same_origin_ip_host = '.'.join(ip_address.split('.')[:2])

origins = [
    "http://localhost",
    "http://localhost:8080",
]

origins.extend([f'http://{same_origin_ip}.{i}:8000' for i in np.arange(2, 255)])
origins.extend([f'http://{same_origin_ip}.{i}:9000' for i in np.arange(2, 255)])
origins.extend([f'http://{same_origin_ip_host}.{i}.{j}:8000' for i, j in
                ((k, l) for k in np.arange(2, 255) for l in np.arange(2, 255))])
origins.extend([f'http://{same_origin_ip_host}.{i}.{j}:9000' for i, j in
                ((k, l) for k in np.arange(2, 255) for l in np.arange(2, 255))])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    thread = RequestThread(db)
    thread.start()
    uvicorn.run(app, host=ip_address, port=8000)
