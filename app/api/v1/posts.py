import logging
import os
from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Security, UploadFile, status, Response
from fastapi_pagination import Page, paginate
from sqlmodel import Session, select
from app.api.v1.authentication import token_decode
from app.core.config import STATIC_DIRECTORY
from app.core.database import get_session
from fastapi import Body
from app.models.posts import Posts
from app.schemas.posts import PostsResponseSchema, PostsSchema

router = APIRouter()

# Configura el registrador
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=PostsSchema)
async def create_post(
    file: UploadFile,
    title: str = Form(...),
    content: Optional[str] = Form(default=None),
    user=Depends(token_decode),
    db: Session = Depends(get_session)
):
    post_data = {
        "title": title,
        "content": content,
    }

    file_path = os.path.join(STATIC_DIRECTORY, file.filename)

    # Guardar el archivo en el servidor
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    db_post = Posts(**post_data, user_id=user.get("sub"), file_path=f"/static/{file.filename}")
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/get_posts", response_model=Page[PostsResponseSchema])
async def get_posts(
    user=Depends(token_decode),
    db: Session = Depends(get_session)
):
    db_posts = db.exec(select(Posts)).all()
    return paginate(db_posts)
