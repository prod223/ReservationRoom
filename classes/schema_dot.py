from pydantic import BaseModel
from datetime import datetime

class MeetingRoom(BaseModel):
    room_name: str
    location: str
    capacity: int
    priceOnHours: float

class Reservation(BaseModel):
    room: MeetingRoom
    start_time: datetime
    end_time: datetime
    user_id: int

class User(BaseModel):
    email: str
    password: str 