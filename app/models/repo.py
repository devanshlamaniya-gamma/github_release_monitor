from sqlalchemy import Column , String , Integer , Boolean , ForeignKey , DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
from app.models.user import User
from datetime import datetime

class repository(Base):

    __tablename__ = "repository"

    id = Column(Integer , primary_key = True , index = True)
    owner = Column(String , nullable = False)
    # repo_name = Column(String , nullable = False)
    name = Column(String , nullable = False)

    # sha = Column(String , nullable= False ,unique=True)
    # message = Column(String , nullable=False)
    # author = Column(String , nullable=False)
    # commit_time = Column(DateTime , nullable=False)
    # user_id  = Column(Integer , ForeignKey(User.id) , nullable=False)
    user_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    
    last_synced_at = Column(DateTime , default= datetime.utcnow)


    user = relationship("User", back_populates="repo")