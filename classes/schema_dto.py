from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class MeetingRoom(BaseModel):
    id: str  # Identifiant unique de l'annonce
    owner_id: str  # Identifiant de l'utilisateur qui a publié l'annonce
    title: str
    description: str
    location: str
    capacity: int
    priceOnHours: float
    click_count: int = 0  # Nombre de clics sur l'annonce
    is_available: bool

class MeetingRoomNoId(BaseModel):
    title: str
    description: str
    location: str
    capacity: int
    priceOnHours: float
    is_available: bool

class Click(BaseModel):
    id: str  # Identifiant unique du clic
    user_id: str  # Identifiant de l'utilisateur qui a effectué le clic
    room_listing_id: int  # Identifiant de l'annonce cliquée
    click_time: datetime  # Date et heure du clic

class User(BaseModel):
    email: str  
    password: str  