from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    
    
class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    
    
class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    
# Base.metadata.create_all(bind=engine)