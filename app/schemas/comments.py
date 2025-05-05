from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    ticket_id: int
    user_id: int


class CommentUpdate(BaseModel):
    content: Optional[str]


class CommentInDB(CommentBase):
    id: int
    created_at: datetime
    ticket_id: int
    user_id: int

    class Config:
        orm_mode = True


class CommentResponse(CommentInDB):
    pass
