import pytest
from src.schemas import UserCreate
from src.repository.users import create_user, get_user_by_email, get_user_by_id, get_user_by_name, update_token
from src.database import models


@pytest.fixture(autouse=True)
def clean_db(session):
    models.Base.metadata.drop_all(bind=session.get_bind())
    models.Base.metadata.create_all(bind=session.get_bind())


@pytest.mark.asyncio
async def test_create_user(session):
    user_data = UserCreate(
        username="testuser", email="test@example.com", password="password123"
    )

    created_user = await create_user(user_data, db=session)

    assert created_user.username == user_data.username
    assert created_user.email == user_data.email
    assert (
        created_user.password == user_data.password
    )


@pytest.mark.asyncio
async def test_get_user_by_email(session):
    user_data = UserCreate(
        username="testuser", email="test@example.com", password="password123"
    )
    await create_user(user_data, db=session)

    user = await get_user_by_email("test@example.com", db=session)

    assert user is not None
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id(session):
    user_data = UserCreate(
        username="testuser", email="test@example.com", password="password123"
    )
    created_user = await create_user(user_data, db=session)

    user = await get_user_by_id(created_user.id, db=session)

    assert user is not None
    assert user.id == created_user.id


@pytest.mark.asyncio
async def test_get_user_by_name(session):

    user_data = UserCreate(
        username="testuser", email="test@example.com", password="password123"
    )
    await create_user(user_data, db=session)

    user = await get_user_by_name("testuser", db=session)

    assert user is not None
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_update_token(session):

    user_data = UserCreate(
        username="testuser", email="test@example.com", password="password123"
    )
    user = await create_user(user_data, db=session)

    new_token = "new_refresh_token"
    await update_token(user, new_token, db=session)

    updated_user = await get_user_by_id(user.id, db=session)
    assert updated_user.refresh_token == new_token
