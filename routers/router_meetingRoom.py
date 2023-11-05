import json
from fastapi import APIRouter, HTTPException
from typing import List
from database.firebse import db

from classes.schema_dto import MeetingRoom, MeetingRoomNoId
import uuid

router = APIRouter(
    prefix='/meetingroom',
    tags=["Meetingroom"]
)

meetingRooms=[]

@router.get('/', response_model=List[MeetingRoom])
async def get_all_meeting_rooms():
    meetingRoomsData = db.child("meetingRooms").get().val()
    if meetingRoomsData:
        # Si des données sont disponibles, convertissez-les en une liste de MeetingRoom
        meeting_rooms_list = []
        for room_id, room_data in meetingRoomsData.items():
            room = MeetingRoom(**room_data)
            room.id = room_id
            meeting_rooms_list.append(room)
        return meeting_rooms_list
    
@router.get('/{meeting_id}', response_model=MeetingRoom)
async def get_meeting_room_by_id(meeting_id: str):
    meetingRoomData = db.child("meetingRooms").child(meeting_id).get().val()
    if meetingRoomData:
        room = MeetingRoom(**meetingRoomData)
        room.id = meeting_id
        return room
    else:
        raise HTTPException(status_code=404, detail="Meeting room not found")

@router.post('/', response_model=MeetingRoom, status_code=201)
async def add_new_meeting_room(given_room: MeetingRoomNoId):
    # Générez un ID unique pour la salle de réunion
    generated_id = uuid.uuid4()

    # Créez une nouvelle instance de la salle de réunion
    new_meeting_room = MeetingRoom(
        id=str(generated_id),
        owner_id=given_room.owner_id,
        title=given_room.title,
        description=given_room.description,
        location=given_room.location,
        capacity=given_room.capacity,
        priceOnHours=given_room.priceOnHours,
        click_count=0,  # Initialisez le nombre de clics à zéro
        is_available=True  # Par défaut, la salle de réunion est disponible
    )

    # Convertissez la salle de réunion en un dictionnaire Python
    meetingRooms.append(new_meeting_room)
    # Stockez le dictionnaire dans la base de données Firebase en tant que JSON
    db.child("meetingRooms").child(str(generated_id)).set(new_meeting_room.model_dump())
    return new_meeting_room


@router.delete('/{meeting_id}', response_model=dict)
async def delete_meeting_room_by_id(meeting_id: str):
    meetingRoomData = db.child("meetingRooms").child(meeting_id).get().val()
    if meetingRoomData:
        # Supprimez la salle de réunion de la base de données Firebase
        db.child("meetingRooms").child(meeting_id).remove()
        return {"message": "Meeting room deleted"}
    else:
        raise HTTPException(status_code=404, detail="Meeting room not found")
    

