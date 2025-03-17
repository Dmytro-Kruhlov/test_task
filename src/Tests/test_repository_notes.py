import pytest

from src.database import models
from src.repository.notes import (
    create_note,
    get_note,
    get_user_notes,
    update_note,
    delete_note,
    create_version,
    get_latest_version_number,
    get_note_versions
)
from src.schemas import NoteCreate, NoteUpdate


@pytest.fixture(autouse=True)
def clean_db(session):
    models.Base.metadata.drop_all(bind=session.get_bind())
    models.Base.metadata.create_all(bind=session.get_bind())


@pytest.mark.asyncio
async def test_create_note(session, user):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=user['id'], db=session)

    assert note.title == note_data.title
    assert note.content == note_data.content
    assert note.user_id == user['id']


@pytest.mark.asyncio
async def test_get_note(session):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=1, db=session)

    retrieved_note = await get_note(note.id, db=session)
    assert retrieved_note is not None
    assert retrieved_note.id == note.id
    assert retrieved_note.title == note_data.title


@pytest.mark.asyncio
async def test_get_user_notes(session, user):
    note_data1 = NoteCreate(title="Test Note 1", content="Content 1")
    note_data2 = NoteCreate(title="Test Note 2", content="Content 2")
    await create_note(note_data1, user_id=user['id'], db=session)
    await create_note(note_data2, user_id=user['id'], db=session)

    notes = await get_user_notes(user['id'], db=session)
    assert len(notes) == 2


@pytest.mark.asyncio
async def test_update_note(session):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=1, db=session)

    update_data = NoteUpdate(title="Updated Test Note", content="Updated content.")
    updated_note = await update_note(note.id, update_data, db=session)

    assert updated_note.title == update_data.title
    assert updated_note.content == update_data.content


@pytest.mark.asyncio
async def test_delete_note(client, session):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=1, db=session)

    result = await delete_note(note.id, db=session)
    assert result is True

    deleted_note = await get_note(note.id, db=session)
    assert deleted_note is None


@pytest.mark.asyncio
async def test_create_version(client, session):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=1, db=session)

    version = await create_version(note.id, note.content, 1, db=session)
    assert version.note_id == note.id
    assert version.content == note.content
    assert version.version_number == 1


@pytest.mark.asyncio
async def test_get_latest_version_number(client, session):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=1, db=session)

    await create_version(note.id, note.content, 1, db=session)
    latest_version_number = await get_latest_version_number(note.id, db=session)

    assert latest_version_number == 1


@pytest.mark.asyncio
async def test_get_note_versions(client, session):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=1, db=session)

    await create_version(note.id, "New content", 2, db=session)
    await create_version(note.id, "Updated content", 3, db=session)

    versions = await get_note_versions(note.id, db=session)
    assert len(versions) == 3
    assert versions[0].version_number == 1
    assert versions[1].version_number == 2
    assert versions[2].version_number == 3