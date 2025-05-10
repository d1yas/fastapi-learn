from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "open"
    priority: str = "medium"


class TicketCreate(TicketBase):
    user_id: int


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class TicketInDB(TicketBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True


class TicketResponse(TicketInDB):
    class Config:
        orm_mode = True
        from_attributes = True  # For newer Pydantic versions


class TicketList(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[TicketResponse]

    class Config:
        orm_mode = True
        from_attributes = True  # For newer Pydantic versions