import bcrypt
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException , status

from app.database.db import get_db
from app.models.user import User
from app.schema.user import UserCreate
from app.authentication.jwt_auth import create_access_token
from app.authentication.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm 
from app.authentication.jwt_auth import oauth2_scheme , decode_access_token
router = APIRouter(prefix= "/router" )


# --------------for registering user 


@router.post("/register" )
def register_user(user : UserCreate , db : Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "this email is already exist"
        )

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8") , bcrypt.gensalt())
    new_user = User(
        email = user.email,
        password = hashed_password.decode("utf-8")
        # password = user.p assword
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    jwt_token = create_access_token({"email" : new_user.email , "user_id" : new_user.id})
    # SECRET_KEY = str(user.email+user.password)
    # ALGORITHM = "HS256"


    return {
        "id" : new_user.id,
        "email" : new_user.email,
        "token" : jwt_token
        
    }



# ----------------------for login 


@router.post("/login")
def login_user(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends() ):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not bcrypt.checkpw(
        form_data.password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    # The key MUST be 'access_token' and 'token_type'
    return {
        "access_token": token, 
        "token_type": "bearer" 
    }



# ---------------------------for gettting all users


@router.get("/users")
def get_users(db : Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    
    # token_check = decode_access_token(token)

    # if not token_check:


        # return "the token is invalid or expired"
    
    # else:
    print("now printing all users")
    return db.query(User).all()



# ----------------------------for getting user by id

@router.get("/users/{id}")
def get_user_id(id : int , db : Session = Depends(get_db),token:str=Depends(oauth2_scheme)):

    print("getting user by id")
    getting_by_id = db.query(User).filter(User.id == id).first()

    

    if not getting_by_id:
        raise HTTPException(404 , "id not found")
    else:

        # token_check = decode_access_token(token)

    # if not token_check:

        
        # return "the token is invalid or expired"
    
    # else:  
        print("got the id")
        return getting_by_id



# ----------------------to see own profile


@router.get("/profile")
def get_profile(current_user : User = Depends(get_current_user)):
    return{
        "user_id" : current_user.id,
        "user_email" : current_user.email
    }