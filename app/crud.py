from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note
from app.schemas import NoteCreate

async def get_notes(db: AsyncSession):
    result = await db.execute(select(Note))
    return result.scalars().all()

async def create_note(db: AsyncSession, note: NoteCreate):
    db_note = Note(**note.dict())
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

async def delete_note(db: AsyncSession, note_id: int):
    note = await db.get(Note, note_id)
    if note:
        await db.delete(note)
        await db.commit()
    return note
