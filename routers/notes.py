from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Response
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

@router.post("/",response_description="Create a new note",response_model=NoteModel)
async def create_note(note: NoteModel):
    new_note=await notes_collection.insert_one(
        note.model_dump(by_alias=True, exclude=["id"])
    )
    created_note=await notes_collection.find_one(
        {"_id":new_note.inserted_id}
    )
    return created_note

@router.get("/",response_description="List first 100 notes",response_model=List[NoteModel])
async def list_notes():
    notes=await notes_collection.find().to_list(100)
    return notes

@router.get("/{id}",response_description="Get a specific note by ID",response_model=NoteModel)
async def get_note_by_id(id:str):
    try:
        note=await notes_collection.find_one({"_id":ObjectId(id)})
        return note
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,detail=f"Note with {id} not found!")

@router.get("/{id}",response_description="Get a specific note by ID",response_model=NoteModel)
async def get_note_by_id(id:str):
    try:
        note=await notes_collection.find_one({"_id":ObjectId(id)})
        return note
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,detail=f"Note with {id} not found!")

@router.delete("/{id}",response_description="Delete a specific note by ID")
async def delete_note_by_id(id:str):
    deleted_note=await notes_collection.delete_one({"_id":ObjectId(id)})
    if deleted_note.deleted_count==1:
        return Response(content=f"Note with ID {id} successfully deleted!",status_code=200)
    raise HTTPException(status_code=404,detail=f"Note with {id} not found!")
