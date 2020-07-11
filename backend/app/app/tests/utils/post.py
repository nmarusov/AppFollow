from typing import Optional
from random import randint

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.post import PostCreate
from app.tests.utils.utils import random_lower_string


def create_random_post(db: Session) -> models.Post:
    title = random_lower_string()
    url = f"http://{random_lower_string()}"
    post_in = PostCreate(title=title, url=url)

    return crud.post.create(db=db, obj_in=post_in)
