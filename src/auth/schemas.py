from pydantic import BaseModel
from sqlmodel import Field
import uuid
from datetime import  datetime


class UserCreateModel(BaseModel):
    first_name:str =Field(max_length=25)
    last_name:str =Field(max_length=25)
    username:str =Field(max_length=8)
    email:str =Field(max_length=100)
    password:str =Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    first_name:str
    last_name:str
    username:str
    email:str
    is_verified:bool
    created_at:datetime

class UserLoginModel(BaseModel):
    email:str =Field(max_length=100)
    password:str =Field(min_length=6)        