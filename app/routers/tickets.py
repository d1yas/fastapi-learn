from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List

from ..schemas.tickets import TicketBase, TicketInDB, TicketCreate, TicketUpdate, TicketResponse, TicketList
from ..core.database import Base, engine, get_db
from sqlalchemy import select, func
from ..models.tickets import TicketsModel
from ..core.dependencies import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

router = APIRouter(prefix='/tickets', tags=['Tickets'])


@router.post('/tickets', response_model=TicketResponse)
async def create_ticket(
        ticket: TicketCreate,
        session: AsyncSession = Depends(get_db)
):
    new_ticket = TicketsModel(
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
        user_id=ticket.user_id
    )
    session.add(new_ticket)
    await session.commit()
    await session.refresh(new_ticket)
    return TicketResponse.from_orm(new_ticket)


@router.get('/tickets', response_model=TicketList)
async def all_tickets(
        session: SessionDep,
        limit: int = Query(default=10, ge=1),
        offset: int = Query(default=0, ge=0),
        status: Optional[str] = Query(default=None),
        priority: Optional[str] = Query(default=None),
        created_at: Optional[str] = Query(default=None)
):
    query = select(TicketsModel)

    if status:
        query = query.where(TicketsModel.status == status)
    if priority:
        query = query.where(TicketsModel.priority == priority)
    if created_at:
        query = query.where(TicketsModel.created_at == created_at)

    # Pagination
    paginated_query = query.offset(offset).limit(limit)

    # Execute query
    result = await session.execute(paginated_query)
    tickets = result.scalars().all()

    # Get total count for pagination
    total_query = select(func.count()).select_from(TicketsModel)
    if status:
        total_query = total_query.where(TicketsModel.status == status)
    if priority:
        total_query = total_query.where(TicketsModel.priority == priority)
    if created_at:
        total_query = total_query.where(TicketsModel.created_at == created_at)

    total_result = await session.execute(total_query)
    total_count = total_result.scalar()

    return TicketList(
        total=total_count,
        limit=limit,
        offset=offset,
        data=tickets
    )


# @router.get("/alltickets", response_model=TicketList)
# async def get_tickets(
#         limit: int = Query(default=10, ge=1),
#         offset: int = Query(default=0, ge=0),
#         db: AsyncSession = Depends(get_db)
# ):
#     # Get paginated tickets
#     result = await db.execute(select(TicketsModel).offset(offset).limit(limit))
#     tickets = result.scalars().all()
#
#     # Get total count
#     total_result = await db.execute(select(func.count()).select_from(TicketsModel))
#     total_tickets = total_result.scalar()  # Use scalar() instead of count()
#
#     return TicketList(
#         total=total_tickets,
#         limit=limit,
#         offset=offset,
#         data=tickets
#     )


@router.get('/tickets/{id}', response_model=TicketResponse)
async def select_ticket(id: int, session: SessionDep):
    query = select(TicketsModel).filter(TicketsModel.id == id)
    result = await session.execute(query)
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket



from sqlalchemy import update, select
from fastapi import HTTPException

@router.patch('/tickets/{id}', response_model=TicketResponse)
async def update_ticket(
    id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    session: AsyncSession = Depends(get_db)
):
    query = select(TicketsModel).where(TicketsModel.id == id)
    result = await session.execute(query)
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = {}
    if title:
        update_data["title"] = title
    if description:
        update_data["description"] = description
    if status:
        update_data["status"] = status
    if priority:
        update_data["priority"] = priority

    if update_data:
        stmt = (
            update(TicketsModel)
            .where(TicketsModel.id == id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()

    updated_ticket = await session.get(TicketsModel, id)
    return updated_ticket
