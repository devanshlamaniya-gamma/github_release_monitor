from fastapi import HTTPException , status , Depends
from sqlalchemy.orm import Session

from app.authentication.jwt_auth import decode_access_token , oauth2_scheme
from app.database.db import get_db
from app.models.user import User


def get_current_user(token:str = Depends(oauth2_scheme) , db : Session= Depends(get_db)):
    
    payload = decode_access_token(token)

    user_id = payload.get("user_id")



    if user_id is None:


        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,

            "invalid token payload"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "user not found"
        )
    

    return user


