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
from models.users import DbPost, DbUser
import os
import shutil
from router.user import get_current_user

app = FastAPI()

router = APIRouter(prefix="/post", tags=["Posts"])

folder = "Post/"
os.makedirs(folder, exist_ok=True)


@router.get("/all_post")
def Get_all(db: Session = Depends(get_db)):
    post = db.query(DbPost).order_by(DbPost.id.desc()).all()

    if not post:
        raise HTTPException(status_code=400, detail="No content  all aviable")
    return post


@router.post("/add_post")
def add_post(
    title: str = Form(...),
    description: str = Form(...),
    content: UploadFile = File(...),
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    file_path = os.path.join(folder, content.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(content.file, buffer)
    post = DbPost(
        user_id=current_user.id, title=title, description=description, content=file_path
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Successfully Posted.."}


## Delte a post
@router.delete("/deletepost{id}")
def delete_post(
    id: int = Path(...),
    current_user: DbUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(DbPost).filter(DbPost.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Not found..")

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only Authenticated user can deleted the post"
        )

    db.delete(post)
    db.commit()

    return {"post": post.id, "messsage": "Successfully deleted"}
