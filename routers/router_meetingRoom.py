from fastapi import APIRouter, HTTPException
from typing import List
import uuid

router = APIRouter(
    prefix='/meetingroom',
    tags=["Meetingroom"]
)

@router.get('/',response_model=dict)
async def get_meetingroom():
    return { "message":" liste des annonces disponibles"}