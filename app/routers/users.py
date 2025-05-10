from fastapi import APIRouter, Depends, HTTPException
from ..schemas.users import UserBase, UserCreate, UserInDB, UserLogin, UserResponse
from ..core.database import Base, engine, get_db
from sqlalchemy import select
from ..models.users import UsersModel
from ..core.dependencies import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
from passlib.hash import bcrypt


router = APIRouter(prefix='/users',tags=['Users'])



@router.get('/users', response_model=list[UserResponse])
async def all_users(session: SessionDep):
    query = select(UsersModel)
    result = await session.execute(query)
    users = result.scalars().all()
    return users



@router.post("/auth/register", response_model=list[UserResponse])
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(UsersModel).where(
        (UsersModel.email == user.email) | (UsersModel.username == user.username)
    ))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = bcrypt.hash(user.password)

    new_user = UsersModel(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return [UserResponse.model_validate(new_user)]

@router.get('/user/{id}')
async def select_user(id: int, session: SessionDep):
    query = select(UsersModel).filter(UsersModel.id == id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# @router.on_event("startup")
# async def startup_event():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)