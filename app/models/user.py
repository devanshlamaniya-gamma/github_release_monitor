from sqlalchemy import Column , String , Integer , TIMESTAMP , Boolean 
from app.database.db import Base
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "users"

    id = Column(Integer , primary_key= True)
    email = Column(String , nullable=False , unique= True)
    password = Column(String, nullable=False)  

    repo = relationship("repository", back_populates="user")

