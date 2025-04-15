from fastapi import FastAPI, HTTPException
import uvicorn
app = FastAPI()

@app.get('/',summary='Home', tags=['Get'])
def root():
    return 'Hello world'


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


@app.get('/books',summary='Books', tags=['Get'])
def read_books():
    return books

@app.get('/books/{id}',summary='Book', tags=['Get'])
def get_book(id: int):
    for book in books:
        if book['id'] == id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')



if __name__ == '__main__':
    uvicorn.run("main:app",reload=True)