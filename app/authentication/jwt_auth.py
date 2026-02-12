import jwt
from datetime import datetime , timedelta
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_TIME_MINS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/router/login")


def create_access_token (data : dict):
    to_encode = data.copy()

    # print("---------------------",to_encode)


    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_TIME_MINS)
    to_encode.update({"exp" : expire})
    # encoded_jwt = jwt.encode( to_encode , SECRET_KEY , ALGORITHM)
    # SECRET_KEY = User.id + User.email


    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , ALGORITHM )

    # print(encoded_jwt)
    return encoded_jwt





def decode_access_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
            return payload
        except jwt.ExpiredSignatureError:
            return "the token is expired , create new token"
        except jwt.InvalidTokenError:
            return "the token is invalid recheck the token"

# decode_access_token(user)


