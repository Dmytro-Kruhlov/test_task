from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.database.models import Note, NoteVersion
from src.schemas import NoteCreate, NoteUpdate


async def create_note(note: NoteCreate, user_id: int, db: Session) -> Note:
    db_note = Note(
        title=note.title,
        content=note.content,
        user_id=user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    # Create initial version
    await create_version(db_note.id, note.content, 1, db)
    return db_note


async def get_note(note_id: int, db: Session) -> Note | None:
    return db.query(Note).filter(Note.id == note_id).first()


async def get_user_notes(user_id: int, db: Session) -> list[Type[Note]]:
    return db.query(Note).filter(Note.user_id == user_id).all()


async def update_note(note_id: int, note_update: NoteUpdate, db: Session) -> Note | None:
    db_note = await get_note(note_id, db)
    if not db_note:
        return None

    if note_update.content is not None:
        latest_version = await get_latest_version_number(note_id, db)
        await create_version(note_id, note_update.content, latest_version + 1, db)

    for field, value in note_update.model_dump(exclude_unset=True).items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)
    return db_note


async def delete_note(note_id: int, db: Session) -> bool:
    db_note = await get_note(note_id, db)
    if not db_note:
        return False
    
    db.delete(db_note)
    db.commit()
    return True


async def create_version(note_id: int, content: str, version_number: int, db: Session) -> NoteVersion:
    version = NoteVersion(
        note_id=note_id,
        content=content,
        version_number=version_number
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


async def get_latest_version_number(note_id: int, db: Session) -> int:
    latest_version = (
        db.query(NoteVersion)
        .filter(NoteVersion.note_id == note_id)
        .order_by(desc(NoteVersion.version_number))
        .first()
    )
    return latest_version.version_number if latest_version else 0


async def get_note_versions(note_id: int, db: Session) -> list[Type[NoteVersion]]:
    return (
        db.query(NoteVersion)
        .filter(NoteVersion.note_id == note_id)
        .order_by(NoteVersion.version_number)
        .all()
    )