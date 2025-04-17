from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Response, BackgroundTasks, UploadFile, File
from fastapi.responses import  StreamingResponse, FileResponse
from pydantic import BaseModel
from authx import AuthX, AuthXConfig
from sqlalchemy import select
from sqlalchemy.ext.asyncio import  create_async_engine , async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import time
import asyncio

import uvicorn
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()


config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_acces_token"
config.JWT_TOKEN_LOCATION = ["cookies"]


security = AuthX(config=config)

engine = create_async_engine('sqlite+aiosqlite:///books.db', echo=True)

new_session = async_sessionmaker(engine,expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
class BookAddSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookAddSchema):
    id: int

class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post("/setup_database",summary='Setup database' ,tags=['SETUP DB'])
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}

@app.post('/books', summary='Add book', tags=['POST'])
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {'ok': True}


@app.get('/books/{id}', summary='Get book', tags=['GET'], response_model=BookSchema)
async def get_book(id: int, session: SessionDep):
    query = select(BookModel).where(BookModel.id == id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if book:
        return book
    raise HTTPException(status_code=404, detail='Book not found')




@app.get('/books', summary='Get all books', tags=['GET'])
async def get_post(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()



class UserLoginSchema(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(creds: UserLoginSchema, response: Response):
    if creds.username == 'test' and creds.password == 'test':
        token = security.create_access_token(uid='12345')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise  HTTPException(status_code=401, detail='Incorrect username or password')


@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "TOP SECRET"}




def sync_task():
    time.sleep(3)
    print("Sync task")

async def async_task():
    time.sleep(3)
    print("Async task")

@app.post("/task")
async def some_route(bg_task: BackgroundTasks):
    # asyncio.create_task(async_task())
    bg_task.add_task(sync_task)
    return {'ok': True}

@app.post('/files')
async def upload_file(uploadded_file: UploadFile):
    file = uploadded_file.file
    file_name = uploadded_file.filename
    with open(file_name, 'wb') as f:
        f.write(file.read())


@app.post('/multi_files')
async def upload_files(uploadded_files: list[UploadFile]):
    for uploadded_file in uploadded_files:
        file = uploadded_file.file
        file_name = uploadded_file.filename
        with open(file_name, 'wb') as f:
            f.write(file.read())


@app.get('/file/{filename}')
async def get_file(filename: str):
    return FileResponse(filename)


def iterfiles(filename: str):
    with open(filename, 'rb') as file:
        while chunk := file.read(1024*1024):
            yield chunk
@app.get('/file/streaming/{filename}')
async def get_streaming_file(filename: str):
    return StreamingResponse(iterfiles(filename), media_type='video/mp4')