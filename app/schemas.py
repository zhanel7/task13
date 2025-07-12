from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteOut(NoteCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

