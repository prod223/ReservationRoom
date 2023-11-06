import json
from fastapi import APIRouter,Depends, HTTPException
from typing import List
from database.firebse import db
from routers.router_auth import get_current_user

from classes.schema_dto import MeetingRoom, MeetingRoomNoId
import uuid

router = APIRouter(
    prefix='/meetingroom',
    tags=["Meetingroom"]
)

meetingRooms=[]

#FONCTION POUR INCREMENTER LE NOMBRE DE CLIQUE
def increment_click_count(meeting_id, user_id):
    current_click_count = db.child("meetingRooms").child(meeting_id).child("click_count").get().val()
    meeting_owner_id = db.child("meetingRooms").child(meeting_id).child("owner_id").get().val()
    if meeting_owner_id != user_id:
        new_click_count = current_click_count + 1
        db.child("meetingRooms").child(meeting_id).update({"click_count": new_click_count})


@router.get('/', response_model=List[MeetingRoom])
async def get_all_meeting_rooms(userData: int = Depends(get_current_user)):
    meetingRoomsData = db.child("meetingRooms").get(userData['idToken']).val()
    if userData and meetingRoomsData:
        # Si des données sont disponibles, convertissez-les en une liste de MeetingRoom
        meeting_rooms_list = []
        for room_id, room_data in meetingRoomsData.items():
            room = MeetingRoom(**room_data)
            room.id = room_id
            meeting_rooms_list.append(room)
        return meeting_rooms_list
    else:
        return []
    
@router.get('/{meeting_id}', response_model=MeetingRoom)
async def get_meeting_room_by_id(meeting_id: str,userData: int = Depends(get_current_user)):
    meetingRoomData = db.child("meetingRooms").child(meeting_id).get(userData['idToken']).val()
    if userData:
        increment_click_count(meeting_id, userData['uid'])
        return meetingRoomData
    else:
        raise HTTPException(status_code=404, detail="Meeting room not found")

@router.post('/', response_model=MeetingRoom, status_code=201)
async def add_new_meeting_room(given_room: MeetingRoomNoId, userData: int = Depends(get_current_user)):
    # Générez un ID unique pour la salle de réunion
    generated_id = uuid.uuid4()
    owner_id = userData['uid']
    
    # Créez une nouvelle instance de la salle de réunion
    new_meeting_room = MeetingRoom(
        id=str(generated_id),
        owner_id=owner_id,
        title=given_room.title,
        description=given_room.description,
        location=given_room.location,
        capacity=given_room.capacity,
        priceOnHours=given_room.priceOnHours,  # Initialisez le nombre de clics à zéro
        is_available=True  # Par défaut, la salle de réunion est disponible
    )

    # Convertissez la salle de réunion en un dictionnaire Python
    meetingRooms.append(new_meeting_room)
    # Stockez le dictionnaire dans la base de données Firebase en tant que JSON
    db.child("meetingRooms").child(str(generated_id)).set(new_meeting_room.model_dump(), userData['idToken'])
    return new_meeting_room

@router.delete('/{meeting_id}', response_model=dict)
async def delete_meeting_room_by_id(meeting_id: str, userData: int = Depends(get_current_user)):
    meetingRoomData = db.child("meetingRooms").child(meeting_id).get(userData['idToken']).val()
    if meetingRoomData:
        # Vérifiez si l'owner_id de la salle de réunion correspond à l'uid de l'utilisateur actuel
        if meetingRoomData.get('owner_id') == userData['uid']:
            # Supprimez la salle de réunion de la base de données Firebase
            db.child("meetingRooms").child(meeting_id).remove()
            return {"message": "Meeting room deleted"}
        else:
            raise HTTPException(status_code=403, detail="Permission denied. You are not the owner of this meeting room")
    else:
        raise HTTPException(status_code=404, detail="Meeting room not found")

    
@router.patch('/{meeting_id}', response_model=MeetingRoom)
async def patch_meeting_room_by_id(meeting_id: str, updated_meeting_room: MeetingRoomNoId,userData: int = Depends(get_current_user)):
    meetingRoomData = db.child("meetingRooms").child(meeting_id).get(userData['idToken']).val()
    if meetingRoomData and meetingRoomData.get('owner_id') == userData['uid']:
        # Mettez à jour partiellement la salle de réunion dans la base de données Firebase
        update_data = {
            "title": updated_meeting_room.title,
            "description": updated_meeting_room.description,
            "location": updated_meeting_room.location,
            "capacity": updated_meeting_room.capacity,
            "priceOnHours": updated_meeting_room.priceOnHours,
        }
        db.child("meetingRooms").child(meeting_id).update(update_data)
        
        updated_meeting_room_data = db.child("meetingRooms").child(meeting_id).get(userData['idToken']).val()
        updated_meeting_room = MeetingRoom(**updated_meeting_room_data)
        return updated_meeting_room
    else:
        raise HTTPException(status_code=404, detail="Meeting room not found")

