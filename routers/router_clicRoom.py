from fastapi import APIRouter, HTTPException
from typing import List
import uuid

router = APIRouter(
    prefix='/clicroom',
    tags=["Clicroom"]
)


@router.get('/',response_model=dict)
async def get_clicroom():
    return { "message":" nombre de clic sur une annonce"}
