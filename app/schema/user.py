# here will be the pydantic classes new folder will create eaxh time for each table

from pydantic import BaseModel , EmailStr

class UserCreate(BaseModel):
    email : EmailStr
    password : str

# class 
#everythign is completed