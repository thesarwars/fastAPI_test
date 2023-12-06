from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    # books = relationship('Book', back_populates = 'author')
    
class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    # author = relationship('Author', back_populates='books')
    clients = relationship("Client", secondary='book_client_link', back_populates="books")
    
class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    # books = relationship('Book', secondary='book_client_link', back_populates='author')
    books = relationship("Book", secondary='book_client_link', back_populates="clients")
    
class BookClientLink(Base):
    __tablename__ = 'book_client_link'
    
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=True)
# Base.metadata.create_all(bind=engine)