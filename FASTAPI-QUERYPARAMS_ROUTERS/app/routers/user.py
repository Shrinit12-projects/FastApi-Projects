from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix= "/users",
    tags = ['Users']
)

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    hash_password= utils.hash_password(user.password)
    user.password = hash_password
    new_user =  models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #this will provide the newly created post *RETURNING in SQL
    return  new_user

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'User with {id} not found ')
    return user