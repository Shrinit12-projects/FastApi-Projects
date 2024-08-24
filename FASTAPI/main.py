from typing import Optional
from fastapi import FastAPI, Response,status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

#######                          this is for validation
class Post(BaseModel):
    title:str  # i want to fix this variable as string
    content: str 
    published: bool = True #here i have provided with a default value 
    rating: Optional[int] = None # this is the optional field and the default value for the value null

my_posts= [{"title": "title of post 1", "content":"content of post 1", "id":1},{"title": "title of post 2 ", "content":"content of post 2", "id":2}]

@app.get('/') # routing to the / ebdpoint
def hello_word():
    return {'message': my_posts}

@app.post('/posts') # routing to the post endpoint 
def create_posts(posts: Post):#here we can call the class post to validate the body tha is being sent to us by the frontend
    print(posts)
    post_dict =  posts.dict()      #the validated boy can be converted to diictionary by .dict()
    post_dict['id']= randrange(0, 100000)
    print(posts)
    my_posts.append(post_dict)
    return {"data": post_dict}
@app.get("/posts/latest")                               #we cant use it here because the posts/{id} is the first match and it will never come tot this endpoint
def latest_posts():                                     #But if we shif this above that then both will work as latest will first match to this and will never come to {id}
    return my_posts[len(my_posts)-1]

@app.get("/posts/{id}") ##using the path parameters
def get_post(id: int, response: Response):  #in order to make surew that id should automatically be converted to an integer
    print(id)
    # id = int(id)
    for posts in my_posts:
        if posts['id'] == id:
            return{"post": posts}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": f'post with {id} was not found'}

# @app.get("/posts/latest")                               we cant use it here because the posts/{id} is the first match and it will never come tot this endpoint
# def latest_posts():                                     But if we shif this above that then both will work as latest will first match to this and will never come to {id}
#     return my_posts[len(my_posts)]