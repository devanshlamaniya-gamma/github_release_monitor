from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = "postgresql://postgres:devansh123@localhost:5432/git_db"
# DATABASE_URL = "postgresql://postgres:devansh123@db:5432/git_db"
# DATABASE_URL = os.getenv("DATABASE_URL")



engine = create_engine (DATABASE_URL) # creating engine to connect with database

SessionLocal = sessionmaker( bind=  engine, autoflush =False, autocommit= False)  # autoflush db m changes hone se prevent krta h , autocommit - commit khud se ni hota apn ko krna pdta h 


Base = declarative_base()


def get_db():
    # db = local_session()
    db = SessionLocal()

    try:

        yield db
    finally:

        db.close()

