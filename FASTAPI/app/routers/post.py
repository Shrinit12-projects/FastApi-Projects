from .. import models, schemas,utils, oauth2
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db

router= APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
) #we can see that every singlr file in this route start with posts so instead we can use prefix

@router.get("/", response_model= List[schemas.Post])
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} doesnt exist')
    post.delete(synchronize_session = False)
    db.commit()    
    return Response(status_code= status.HTTP_204_NO_CONTENT)    

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.Post) # routing to the post endpoint ##also if i pass the status code in here then it will return the status code once success ful
def create_posts(posts: schemas.PostCreate, db: Session =  Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):#here we can call the class post to validate the body tha is being sent to us by the frontend
    print(user_id)
    new_post =  models.Post(**posts.dict()) #this will unpack the dictionary and if multiple new columns are added then it will doe it
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #this will provide the newly created post *RETURNING in SQL
    return  new_post


@router.get("/{id}", response_model= schemas.Post) ##using the path parameters
def get_post(id: int, db: Session= Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):  #in order to make surew that id should automatically be converted to an integer
    print(id)
    specificpost = db.query(models.Post).filter(models.Post.id == id).first() #we can do .all() but then it will go through all the data
    if not specificpost:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} was not found') # i replaced the entire thing above with this this will raise an http 404 exception
    return specificpost
# @app.get("/posts/latest")                               we cant use it here because the posts/{id} is the first match and it will never come tot this endpoint
# def latest_posts():                                     But if we shif this above that then both will work as latest will first match to this and will never come to {id}
#     return my_posts[len(my_posts)]

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= schemas.Post)
def update_posts(id: int, update: schemas.PostCreate, db: Session= Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'post with {id} was not found')
    post_query.update( update.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()
