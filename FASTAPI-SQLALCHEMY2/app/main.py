#good to know
    #whenever we create a new folder for python we create a file __init__.py to add all the packages and we leave it empty for now



import re
from typing import Optional, List
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

while True:
    try:
        conn = psycopg2.connect(host='localhost',database = 'postgres', user= 'postgres',password ='Password123', cursor_factory= RealDictCursor)                             #(host, database, user, password)
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

@app.get("/posts", response_model= List[schemas.Post])
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} doesnt exist')
    post.delete(synchronize_session = False)
    db.commit()    
    return Response(status_code= status.HTTP_204_NO_CONTENT)    

@app.post('/posts', status_code= status.HTTP_201_CREATED, response_model= schemas.Post) # routing to the post endpoint ##also if i pass the status code in here then it will return the status code once success ful
def create_posts(posts: schemas.PostCreate, db: Session =  Depends(get_db)):#here we can call the class post to validate the body tha is being sent to us by the frontend
    new_post =  models.Post(**posts.dict()) #this will unpack the dictionary and if multiple new columns are added then it will doe it
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #this will provide the newly created post *RETURNING in SQL
    return  new_post



@app.get("/posts/latest")                               #we cant use it here because the posts/{id} is the first match and it will never come tot this endpoint
def latest_posts():                                     #But if we shif this above that then both will work as latest will first match to this and will never come to {id}
    return my_posts[len(my_posts)-1]




@app.get("/posts/{id}", response_model= schemas.Post) ##using the path parameters
def get_post(id: int, db: Session= Depends(get_db)):  #in order to make surew that id should automatically be converted to an integer
    print(id)
    specificpost = db.query(models.Post).filter(models.Post.id == id).first() #we can do .all() but then it will go through all the data
    if not specificpost:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} was not found') # i replaced the entire thing above with this this will raise an http 404 exception
    return specificpost
# @app.get("/posts/latest")                               we cant use it here because the posts/{id} is the first match and it will never come tot this endpoint
# def latest_posts():                                     But if we shif this above that then both will work as latest will first match to this and will never come to {id}
#     return my_posts[len(my_posts)]

@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model= schemas.Post)
def update_posts(id: int, update: schemas.PostCreate, db: Session= Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} was not found')
    post_query.update( update.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()


                   #

@app.post('/users', status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user =  models.User(**user.dict()) #this will unpack the dictionary and if multiple new columns are added then it will doe it
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #this will provide the newly created post *RETURNING in SQL
    return  new_user

