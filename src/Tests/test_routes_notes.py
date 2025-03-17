from unittest.mock import patch

import pytest
from src.schemas import NoteCreate, NoteUpdate
from src.repository.notes import create_note
from src.services.auth import auth_service


@pytest.fixture(autouse=True)
def mock_redis_db():
    with patch.object(auth_service, "redis_db") as redis_mock:
        redis_mock.get.return_value = None
        yield redis_mock


@pytest.fixture()
def token(client, user, session):
    client.post("/api/auth/signup", json=user)

    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


@pytest.mark.skip("failed as radis")
@pytest.mark.asyncio
async def test_create_note(client, token):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")

    response = client.post(
        "api/notes/",
        json=note_data.model_dump(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    created_note = response.json()
    assert created_note["title"] == note_data.title
    assert created_note["content"] == note_data.content


@pytest.mark.asyncio
async def test_get_note(client, session, user):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=user["id"], db=session)

    response = client.get(f"api/notes/{note.id}")

    assert response.status_code == 200
    retrieved_note = response.json()
    assert retrieved_note["id"] == note.id
    assert retrieved_note["title"] == note_data.title


@pytest.mark.asyncio
async def test_update_note(client, session, user):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=user["id"], db=session)

    update_data = NoteUpdate(title="Updated Test Note", content="Updated content.")
    response = client.put(f"api/notes/{note.id}", json=update_data.model_dump())

    assert response.status_code == 200
    updated_note = response.json()
    assert updated_note["title"] == update_data.title
    assert updated_note["content"] == update_data.content


@pytest.mark.asyncio
async def test_delete_note(client, session, user):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = await create_note(note_data, user_id=user["id"], db=session)

    response = client.delete(f"api/notes/{note.id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Note deleted successfully"}

    response = client.get(f"/notes/{note.id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_notes_analytics(client):
    response = client.get("api/notes/analytics/stats")

    assert response.status_code == 200
    analytics_data = response.json()
    assert "total_word_count" in analytics_data
    assert "average_note_length" in analytics_data
    assert "most_common_words" in analytics_data
