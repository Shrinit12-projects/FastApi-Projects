#good to know
    #whenever we create a new folder for python we create a file __init__.py to add all the packages and we leave it empty for now
from fastapi import FastAPI
from app import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)