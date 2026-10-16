from alembic.util import status
from fastapi import (
    FastAPI,
    Form,
    File,
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    Path,
)
from fastapi.security import OAuth2
from sqlalchemy.orm import Session
from database.db import get_db
from models.users import DbPost, DbUser, Dbcomment
import os
import shutil
from router.user import get_current_user


app = FastAPI()


router = APIRouter(prefix="/comment", tags=["Comment"])


### Get all comment


#### User path for id just in case of check exist or not
@router.get("/comment/{id}")
def get_all(id: int = Path(...), db: Session = Depends(get_db)):
    comment = db.query(Dbcomment).filter(Dbcomment.id == id).first()
    if not comment:
        raise HTTPException(status_code=400, detail="No comment are available now..")

    user_comment = db.query(Dbcomment).order_by(Dbcomment.id.desc()).all()

    return user_comment


### create comment
@router.post("/add_comment/")
def create_comment(
    text: str = Form(...),
    post_id: int = Form(...),
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = Dbcomment(
        post_id=post_id,
        text=text,
        username=current_user.username,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
