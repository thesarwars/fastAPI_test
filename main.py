from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from models import *
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class BaseBook(BaseModel):
    title: str
    author_id: int
    
            
@app.post('/authors/')
async def add_authors(full_name: str, db: Session=Depends(get_db)):
    try:
        author = Author(full_name=full_name)
        db.add(author)
        db.commit()
        db.refresh(author)
        return {'msg': 'Author added successfully'}
    except SQLAlchemyError as e:
        db.rollback()
        return {'error': str(e)}
    finally:
        db.close()

# @app.get('/auth-list')
# async def author_list(full_name: str, db: Session=Depends(get_db)):

@app.post('/books/')
async def add_books(title: str, author_id: int, db: Session=Depends(get_db)):
    book = Book(title=title, author_id=author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return {'msg': 'Book added successfully'}
    
    
# @app.patch('/books/{book_id}', response_model=Book)
# async def edit_book(self, book_id: int, title: str, author_id: int, db: Session(get_db)):
#     book = db.query(Book).get(book_id)
#     if book:
#         book.title = title
#         book.author_id = author_id
#         db.commit()
#         db.refresh(book)
#         return book.dict()
#     raise HTTPException(status_code=400, detail="Book not found")

@app.put('/books/{book_id}', response_model=Book)
async def edit_book(book_id: int, book: Book, db: Session=Depends(get_db)):
    db_book = db.query(Book).filter(Book,id==book_id).first()
    if db_book:
        db_book.title = book.title
        db_book.author_id = book.author_id
        db.commit()
        db.refresh(db_book)
        return db.book
    raise HTTPException(status_code=400, detail="Book not found")

@app.get('/books/')
async def get_book(starts_with: str = "", author: str = "", db: Session=Depends(get_db)):
    query = db.query(Book)
    if starts_with:
        query = query.filter(Book.title.startswith(starts_with))
    if author:
        query = query.join(Author).filter(Author.full_name==author)
    return query.all()       