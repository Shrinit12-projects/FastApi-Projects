from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}" #"postgresql://<username>:<password>@<ip-address>/<hostname>/<database_name>"

engine = create_engine(SQLALCHEMY_DATABASE_URL) #engine is what is responsible for sql alchemy to connect to postgres database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def get_db():
    db = SessionLocal() # line 17 to line 20 is or creating a session in the database
    try:
        yield db
    finally:
        db.close()