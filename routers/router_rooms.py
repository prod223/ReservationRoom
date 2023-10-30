from fastapi import APIRouter, HTTPException
from typing import List
import uuid

router = APIRouter(
    prefix='/courses',
    tags=["Courses"]
)



@router.get('', response_model=List)
async def get_courses():
    """List all the courses."""
    return { "message":" liste of room"}
