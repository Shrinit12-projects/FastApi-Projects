from click import password_option
from pydantic import BaseModel, EmailStr
from datetime import datetime
#######                          this is for validation
# this is the optional field and the default value for the value null


class PostBase(BaseModel):
    title:str  # i want to fix this variable as string
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    
    class config:
        orm_mode = True