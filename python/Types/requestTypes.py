from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GetTemperature:
    id: int
    HID: str


@dataclass
class GetTemperatures:
    HID: str
    offset: int
    limit: int


@dataclass
class CreateTemperature:
    time: datetime
    temp_c: float
    temp_f: float
    HID: str


@dataclass
class UpdateTemperature:
    id: int
    HID: str
    temp_c: Optional[float] = None
    temp_f: Optional[float] = None


@dataclass
class DeleteTemperature:
    id: int
    HID: str


@dataclass
class DeleteTemperatures:
    temp_ids: list[int]
    HID: str


@dataclass
class GetUser:
    username: str
    password: str


@dataclass
class GetUsers:
    HID: str


@dataclass
class CreateUser:
    username: str
    password: str
    token: str


@dataclass
class UserToDelete(dict):
    username: str
    password: str


@dataclass
class UserDeleting(dict):
    username: str
    password: str


@dataclass
class DeleteUser:
    user_to_delete: UserToDelete
    user_deleting: UserDeleting


@dataclass
class GetHID:
    username: str
    password: str
