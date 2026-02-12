from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.db import Base
from app.models.repo import repository

class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    sha = Column(String, nullable=False, unique=True)
    email = Column(String , nullable= False)
    message = Column(String, nullable=False)
    author = Column(String, nullable=False)
    commit_time = Column(DateTime, nullable=False)
    repo_id = Column(Integer, ForeignKey(repository.id), nullable=False)