from typing import Annotated, Optional
import uuid
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class NoteModel(BaseModel):
    id: Optional[PyObjectId]=Field(alias="_id",default=None)
    title: str
    description: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Note-1",
                "description": "This is my first note",
            }
        },
    )