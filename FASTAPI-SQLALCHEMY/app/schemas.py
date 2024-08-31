from pydantic import BaseModel

#######                          this is for validation
class Post(BaseModel):
    title:str  # i want to fix this variable as string
    content: str
    published: bool = True #here i have provided with a default value 
    # rating: Optional[int] = None # this is the optional field and the default value for the value null

class UpdatePost(BaseModel):
    title: str