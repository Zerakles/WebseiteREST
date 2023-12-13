from sqlite3 import Date
from typing import Optional

from pydantic import BaseModel


class TemperatureTable(BaseModel):
    __tablename__ = "temperatures"
    id: int
    time: Date
    temp_c: float
    temp_f: float
    HID: str


class TempReading(BaseModel):
    temp_c: float
    temp_f: float
    HID: str


class UsersTable(BaseModel):
    __tablename__ = "users"
    username: str
    password: str
    HID: str
    token: Optional[str] = None
