from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    id: int
    created_at: datetime


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteVersion(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    id: int
    version_number: int
    content: str
    created_at: datetime


class Note(NoteBase):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    ai_summary: Optional[str] = None
    versions: List[NoteVersion] = []


class NoteAnalytics(BaseModel):
    total_word_count: int
    average_note_length: float
    most_common_words: list[tuple[str, int]]
    longest_notes: List[Note]
    shortest_notes: List[Note]


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
