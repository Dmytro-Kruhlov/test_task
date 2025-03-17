from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import notes as notes_repository
from src.services.analytics import AnalyticsService
from src.services import ai as ai_service
from src.schemas import Note, NoteCreate, NoteUpdate, NoteAnalytics, NoteVersion
from src.services.auth import auth_service
from src.database import models

router = APIRouter(prefix="/notes", tags=["notes"])


gemini_model = ai_service.setup_gemini()


@router.post("/", response_model=Note)
async def create_note(note: NoteCreate, current_user: models.User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    db_note = await notes_repository.create_note(note, current_user.id, db)

    summary = await ai_service.generate_summary(note.content, model=gemini_model)
    if summary:
        db_note.ai_summary = summary
        db.commit()

    return db_note


@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: int, db: Session = Depends(get_db)):
    note = await notes_repository.get_note(note_id, db)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/user/{user_id}", response_model=List[Note])
async def get_user_notes(user_id: int, db: Session = Depends(get_db)):
    return await notes_repository.get_user_notes(user_id, db)


@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)
):
    updated_note = await notes_repository.update_note(note_id, note_update, db)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if note_update.content:
        summary = await ai_service.generate_summary(note_update.content, model=gemini_model)
        if summary:
            updated_note.ai_summary = summary
            db.commit()

    return updated_note


@router.delete("/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    if not await notes_repository.delete_note(note_id, db):
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}


@router.get("/{note_id}/versions", response_model=List[NoteVersion])
async def get_note_versions(note_id: int, db: Session = Depends(get_db)):
    note = await notes_repository.get_note(note_id, db)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return await notes_repository.get_note_versions(note_id, db)


@router.get("/analytics/stats", response_model=NoteAnalytics)
def get_notes_analytics(db: Session = Depends(get_db)):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_notes_analytics()
