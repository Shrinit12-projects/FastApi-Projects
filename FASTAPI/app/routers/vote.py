from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..schemas import Vote
from .. import database, oauth2,models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",
    tags= ['vote']
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(votes: Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "post not found")
    

    vote_query = db.query(models.Votes).filter(models.Votes.post_id ==votes.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (votes.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,detail=f"{current_user.id} already voted on {votes.post_id}")
        new_vote = models.Votes(post_id= votes.post_id, user_id  = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Sucessfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = 'Vote doesnot exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":
                "sucessfully deleted the vote"}