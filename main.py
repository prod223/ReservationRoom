from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

app = FastAPI(
    title="MeetingRoom Reservation",
    description=api_description,
    openapi_tags=tags_metadata
)

@app.get("/")
async def root():
    return { "message" : "Hello World"}