from fastapi import APIRouter, HTTPException
from typing import List
import uuid

router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)

@router.get('/',response_model=dict)
async def get_auth():
    return { "message":"auth"}