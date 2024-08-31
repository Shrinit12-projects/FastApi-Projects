from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm #check line 10 
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags= ['Authentication'])

@router.post('/login', response_model= schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session= Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    #{
    # "username": "ufuufva"
    # "password": "uiboieubv"
    # }
    #also we have to pass the body as form-data instead of body json
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, details = f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, details = f"Invalid Credentials")

    # create a token and return a token
    #pip install python-jose[cryptography]
    # go to ..oauth.py
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"} 