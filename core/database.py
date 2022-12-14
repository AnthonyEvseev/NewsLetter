from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def connect_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
