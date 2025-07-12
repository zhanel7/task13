from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session, engine, Base
from app import crud, schemas, cache

app = FastAPI()

async def get_db():
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/notes", response_model=list[schemas.NoteOut])
async def read_notes(db: AsyncSession = Depends(get_db)):
    cache_key = "notes:all"
    cached_data = await cache.get_cached_notes(cache_key)
    if cached_data:
        return cached_data

    notes = await crud.get_notes(db)
    result = [schemas.NoteOut.from_orm(n) for n in notes]
    await cache.set_cached_notes(cache_key, [r.dict() for r in result])
    return result

@app.post("/notes", response_model=schemas.NoteOut)
async def create_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    created = await crud.create_note(db, note)
    await cache.invalidate_notes_cache("notes:")
    return schemas.NoteOut.from_orm(created)

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    await cache.invalidate_notes_cache("notes:")
    return {"detail": "Note deleted"}
