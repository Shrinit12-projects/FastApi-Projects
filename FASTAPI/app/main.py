#good to know
    #whenever we create a new folder for python we create a file __init__.py to add all the packages and we leave it empty for now



from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()



#######                          this is for validation
class Post(BaseModel):
    title:str  # i want to fix this variable as string
    content: str 
    published: bool = True #here i have provided with a default value 
    # rating: Optional[int] = None # this is the optional field and the default value for the value null

class UpdatePost(BaseModel):
    title: str

while True:
    try:
        conn = psycopg2.connect(host='localhost',database = 'fastapi', user= 'postgres',password ='Simba@1805', cursor_factory= RealDictCursor)                             #(host, database, user, password)
        cursor = conn.cursor()
        print('the database connection was sucessfull')
        break
    except Exception as error:
        print(f'error:{error}')
        time.sleep(2)

my_posts= [{"title": "title of post 1", "content":"content of post 1", "id":1},{"title": "title of post 2 ", "content":"content of post 2", "id":2}]

def delete_id(id):
    i=0
    for post in my_posts:
        if post['id']== id:
            return i
        i=i+1
            
def find_post_index(id: int):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i
    return None




@app.get('/') # routing to the / ebdpoint
def hello_word():
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall
    return {'message': posts}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    i = delete_id(id)
    if i == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} doesnt exist')
    my_posts.pop(i)
    return Response(status_code= status.HTTP_204_NO_CONTENT)    

@app.post('/posts', status_code= status.HTTP_201_CREATED) # routing to the post endpoint ##also if i pass the status code in here then it will return the status code once success ful
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
    # response.status_code = status.HTTP_404_NOT_FOUND  #you can use this to give the message and the status code
    # return {"message": f'post with {id} was not found'}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} was not found') # i replaced the entire thing above with this this will raise an http 404 exception

# @app.get("/posts/latest")                               we cant use it here because the posts/{id} is the first match and it will never come tot this endpoint
# def latest_posts():                                     But if we shif this above that then both will work as latest will first match to this and will never come to {id}
#     return my_posts[len(my_posts)]

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_posts(id: int, update: UpdatePost):
    i = find_post_index(id)
    if i is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} does not exist')

    my_posts[i]['title'] = update.title  # only updating the title as per UpdatePost schema
    return {"message": "Post updated successfully", "post": my_posts[i]}