from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
#######                          this is for validation
# this is the optional field and the default value for the value null


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    
    class config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title:str  # i want to fix this variable as string
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserOut

    class config:
        orm_mode = True



# we have to set up a schema for the access token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]= None    