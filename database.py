from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta 

URL_DATABASE = 'postgresql://postgres:test123456@localhost:5432/TestAPI'

engine = create_engine(URL_DATABASE)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base: DeclarativeMeta = declarative_base()