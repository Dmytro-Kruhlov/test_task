from fastapi import APIRouter, Depends
from src.database import models
from src.services.auth import auth_service
from src import schemas


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(auth_service.get_current_user),
) -> models.User:
    return current_user

