from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel
from typing import List, Annotated, Union
from models import *
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

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

@app.put('/books/{book_id}', response_model=None)
async def edit_book(book_id: int, book: BaseBook, db: Session=Depends(get_db)):
    db_book = db.query(Book).filter(Book.id==book_id).first()
    if db_book:
        db_book.title = book.title
        db_book.author_id = book.author_id
        db.commit()
        db.refresh(db_book)
        return {'msg': 'Update successfully'}
    raise HTTPException(status_code=400, detail="Book not found")

@app.get('/books/')
async def get_book(starts_with: str = "", author: str = "", db: Session=Depends(get_db)):
    query = db.query(Book)
    if starts_with:
        query = query.filter(Book.title.startswith(starts_with))
    if author:
        query = query.join(Author).filter(Author.full_name==author)
    return query.all()


@app.post('/clients/')
async def create_client(full_name: str, db: Session=Depends(get_db)):
    client = Client(full_name=full_name)
    db.add(client)
    db.commit()
    db.refresh(client)
    return {'msg': 'Client Create Successfully'}


oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_token(client_id: int):
    return {'access_token': f"Bearer {client_id}", "token_type": "bearer"}

def def_current_user(token: str = Depends(oauth_scheme)):
    client_id = int(token.split(" ")[1])
    return client_id

@app.get('/clients/book/', response_model=List[BaseBook])
def get_books_borrowed_by_client(current_user: int = Depends(def_current_user), db: Session=Depends(get_db)):
    client_book = db.query(Book).join(Client.books).filter(Client.id==current_user).all()
    return client_book

@app.post('/clients/link_book/{book_id}', response_model=BaseBook)
def link_client_to_book(book_id: int, current_user: int = Depends(def_current_user), db: Session=Depends(get_db)):
    db_book = db.query(Book).filter(Book.id==book_id).first()
    if db_book:
        db_client = db.query(Client).filter(Client.id==current_user).first()
        if db_client:
            db_client.books.append(db_book)
            db.commit()
            db.refresh(db_book)
            return db_book
        else:
            raise HTTPException(status_code=404, detail='Client not found')
    raise HTTPException(status_code=404, detail='Book not found')

@app.post("/clients/unlink_book/{book_id}")
def unlink_client_from_book(book_id: int, current_user: int = Depends(def_current_user), db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        # Unlink the client from the book by removing the book from the client's list of borrowed books
        db_client = db.query(Client).filter(Client.id == current_user).first()
        if db_client:
            db_client.borrowed_books.remove(db_book)
            db.commit()
            return {"message": "Book unlinked successfully"}
        else:
            raise HTTPException(status_code=404, detail="Client not found")
    raise HTTPException(status_code=404, detail="Book not found")