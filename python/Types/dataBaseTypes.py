from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.v1.dataclasses import dataclass


@dataclass
class TemperatureTable(BaseModel):
    __tablename__ = "temperatures"
    id: int
    time: datetime
    temp_c: float
    temp_f: float
    HID: str


@dataclass
class TempReading(BaseModel):
    temp_c: float
    temp_f: float
    HID: str

@dataclass
class UsersTable(BaseModel):
    __tablename__ = "users"
    username: str
    password: str
    HID: str
    token: Optional[str] = None
