from fastapi import APIRouter
import os
import motor.motor_asyncio
from dotenv import load_dotenv

from models.notes import NoteModel


load_dotenv()

mongodb_connection_string=os.getenv("MONGODB_CONNECTION_STRING")
mongodb_client=motor.motor_asyncio.AsyncIOMotorClient(mongodb_connection_string)
db=mongodb_client.get_database("notes_db")
notes_collection=db.get_collection("notes")

router=APIRouter()

@router.post("/v1/notes/")
async def create_note(note: NoteModel):
    return note.dict()
    new_note=await notes_collection.insert_one(
        note.dict()
    )
    new_note_id=new_note.inserted_id
    return new_note_id
