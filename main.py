from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
        
        
@app.post('/authors')
async def add_authors(full_name: str, db: Session=Depends(get_db)):
    author = models.Author(full_name=full_name)
    db.add(author)
    db.commit()
    return {'msg': 'Author added successfully'}


        