from fastapi import APIRouter, HTTPException, UploadFile
from sqlalchemy import select
from fastapi import FastAPI, Depends, HTTPException, Response, BackgroundTasks, UploadFile, File
from src.core.security import security, config
from src.api.dependencies import SessionDep
from fastapi.responses import  StreamingResponse, FileResponse
from src.database import engine, Base
from src.models.books import BookModel
from src.schemas.books import BookSchema, BookAddSchema
from src.schemas.users import UserLoginSchema
import time

router = APIRouter()
@router.post("/setup_database",summary='Setup database' ,tags=['SETUP DB'])
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}

@router.post('/books', summary='Add book', tags=['POST'])
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {'ok': True}


@router.get('/books/{id}', summary='Get book', tags=['GET'], response_model=BookSchema)
async def get_book(id: int, session: SessionDep):
    query = select(BookModel).where(BookModel.id == id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if book:
        return book
    raise HTTPException(status_code=404, detail='Book not found')




@router.get('/books', summary='Get all books', tags=['GET'])
async def get_post(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()





@router.post('/login')
def login(creds: UserLoginSchema, response: Response):
    if creds.username == 'test' and creds.password == 'test':
        token = security.create_access_token(uid='12345')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise  HTTPException(status_code=401, detail='Incorrect username or password')


@router.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "TOP SECRET"}




def sync_task():
    time.sleep(3)
    print("Sync task")

async def async_task():
    time.sleep(3)
    print("Async task")

@router.post("/task")
async def some_route(bg_task: BackgroundTasks):
    # asyncio.create_task(async_task())
    bg_task.add_task(sync_task)
    return {'ok': True}

@router.post('/files')
async def upload_file(uploadded_file: UploadFile):
    file = uploadded_file.file
    file_name = uploadded_file.filename
    with open(file_name, 'wb') as f:
        f.write(file.read())


@router.post('/multi_files')
async def upload_files(uploadded_files: list[UploadFile]):
    for uploadded_file in uploadded_files:
        file = uploadded_file.file
        file_name = uploadded_file.filename
        with open(file_name, 'wb') as f:
            f.write(file.read())


@router.get('/file/{filename}')
async def get_file(filename: str):
    return FileResponse(filename)


def iterfiles(filename: str):
    with open(filename, 'rb') as file:
        while chunk := file.read(1024*1024):
            yield chunk
@router.get('/file/streaming/{filename}')
async def get_streaming_file(filename: str):
    return StreamingResponse(iterfiles(filename), media_type='video/mp4')