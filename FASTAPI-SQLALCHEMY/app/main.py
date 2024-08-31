#good to know
    #whenever we create a new folder for python we create a file __init__.py to add all the packages and we leave it empty for now



from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}





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
############################################# SQLALCHEMY
    #db.query(models.Post).filter(models.Post.id == id)  it will return the first instance   
    #if post.first() == None:
        #  raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} doesnt exist')
    # psot.delete(synchronize_session = False)
    # db.commit()    
@app.post('/posts', status_code= status.HTTP_201_CREATED) # routing to the post endpoint ##also if i pass the status code in here then it will return the status code once success ful
def create_posts(posts: schemas.Post):#here we can call the class post to validate the body tha is being sent to us by the frontend
    print(posts)
    post_dict =  posts.dict()      #the validated boy can be converted to diictionary by .dict()
    post_dict['id']= randrange(0, 100000)
    print(posts)
    my_posts.append(post_dict)
    return {"data": post_dict}

    #add post using sqlalchemy
    #new_post= models.Post(title = post.title, content = post.content, published = post.published)
            #can also be done
            #new_post =  models.Post(**post.dict()) this will unpack the dictionary and if multiple new columns are added then it will doe it
    #db.add(new_post)
    #db.commit()
    #db.refresh(new_post) this will provide the newly created post



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


############################################## SQLALCHEMY
    #db.query(models.Post).filter(models.Post.id == id).first()  it will return the first instance   
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} was not found') # i replaced the entire thing above with this this will raise an http 404 exception

# @app.get("/posts/latest")                               we cant use it here because the posts/{id} is the first match and it will never come tot this endpoint
# def latest_posts():                                     But if we shif this above that then both will work as latest will first match to this and will never come to {id}
#     return my_posts[len(my_posts)]

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_posts(id: int, update: schemas.UpdatePost):
    i = find_post_index(id)
    if i is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} does not exist')

    my_posts[i]['title'] = update.title  # only updating the title as per UpdatePost schema
    return {"message": "Post updated successfully", "post": my_posts[i]}
##################################### SQLALCHEMY
#   post_query = db.query(models.Post).filter(models.Post.ids == id)
#   posts = post_query.first()
#   if posts == None:
    # raise error
#   post_query.update('title':'hiii sqlalchemy', 'content':'wertyuio', synchronize_session = False)
                        #posts.dict()#


@app.get("/sqlalchemy")
def test(db: Session = Depends(get_db)):
    posts = db.query(models.post).all()
    return {"status":"success", "data": posts}