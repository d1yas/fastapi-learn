from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field, ConfigDict


app = FastAPI()


books = [
    {
        'id': 1,
        'title': 'Roadmap Django',
        'author': 'roadmap.sh',
    },
    {
        'id': 2,
        'title': 'Roadmap FastAPI',
        'author': 'solvit',
    }
]


@app.get('/books',summary='Get all books', tags=['Get'])
def read_books():
    return books

@app.get('/books/{id}',summary='Get book', tags=['Get'])
def get_book(id: int):
    for book in books:
        if book['id'] == id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')



class NewBook(BaseModel):
    title: str
    author: str

@app.post('/books/', tags=['Post'])
def create_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author,
    })

    return {'success': 201, "message": "Book created successfully"}
    # return new_book




data = {
    "email": 'abc@gmail.com',
    "bio": None,
    "age": 17,
}


data_wo_age = {
    "email": 'abc@gmail.com',
    "bio": None,
    'gender': 'male',
    'birthday': '2000'
}


def func(data_: dict):
    data_["age"] += 1



class UserSchema(BaseModel):
    email: str
    bio: str | None = Field(max_length=10)
    # age: int = Field(ge=0, le=130)
    model_config = ConfigDict(extra='forbid')

users = []
@app.post('/users', tags=['Post'])
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "message": "User added successfully"}

@app.get('/users', tags=['Get'])
def get_users() -> list[UserSchema]:
    return users

# class UserAgeSchema(BaseModel):
#     age: int


# print(repr(UserSchema(**data_wo_age)))
# print(repr(UserAgeSchema(**data)))




if __name__ == '__main__':
    uvicorn.run("main:app",reload=True)
