from pydantic import BaseModel
from datetime import datetime


class AttachmentBase(BaseModel):
    filename: str
    file_path: str


class AttachmentCreate(AttachmentBase):
    ticket_id: int


class AttachmentInDB(AttachmentBase):
    id: int
    uploaded_at: datetime
    ticket_id: int

    class Config:
        orm_mode = True


class AttachmentResponse(AttachmentInDB):
    pass
