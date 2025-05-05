from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    title: str = Field(..., example="Server ishlamayapti")
    description: str = Field(..., example="Men serverga kira olmayapman")
    status: Optional[str] = Field(default="open")
    priority: Optional[str] = Field(default="medium")


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]


class TicketInDB(TicketBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TicketResponse(TicketInDB):
    pass
