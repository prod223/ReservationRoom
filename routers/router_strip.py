from fastapi import APIRouter, HTTPException
from typing import List
import uuid

router = APIRouter(
    prefix='/stripe',
    tags=["Stripe"]
)

@router.get('/',response_model=dict)
async def get_strip():
    return { "message":" facturation sur strip"}