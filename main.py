from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# @app.get('/',summary='Home', tags=['Get'])
# def root():
#     return 'Hello world'


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

if __name__ == '__main__':
    uvicorn.run("main:app",reload=True)