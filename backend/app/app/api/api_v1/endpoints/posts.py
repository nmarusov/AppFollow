from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Post])
def read_posts(
    db: Session = Depends(deps.get_db),
    offset: int = Query(0, description="Number of skipped posts", ge=0),
    limit: int = Query(5, description="Maximum number of posts", ge=1, le=100),
    order: schemas.PostColumns = Query(
        schemas.PostColumns.id,
        description="Specifies the column by which records being sorted",
    ),
    direction: schemas.SortDirection = Query(
        schemas.SortDirection.ascending, description="Sorting direction"
    ),
) -> Any:
    """
    Retrieve posts.
    """
    posts = crud.post.get_multi(
        db, skip=offset, limit=limit, order_by=order.value, direction=direction.value
    )
    return posts


# @router.post("/", response_model=schemas.Post)
# def create_post(
#     *, db: Session = Depends(deps.get_db), post_in: schemas.PostCreate
# ) -> Any:
#     """
#     Create new post.
#     """
#     post = crud.post.create(db=db, obj_in=post_in)
#     return post


# @router.put("/{id}", response_model=schemas.Post)
# def update_post(
#     *, db: Session = Depends(deps.get_db), id: int, post_in: schemas.PostUpdate
# ) -> Any:
#     """
#     Update an post.
#     """
#     post = crud.post.get(db=db, id=id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     post = crud.post.update(db=db, db_obj=post, obj_in=post_in)
#     return post


# @router.get("/{id}", response_model=schemas.Post)
# def read_post(*, db: Session = Depends(deps.get_db), id: int) -> Any:
#     """
#     Get post by ID.
#     """
#     post = crud.post.get(db=db, id=id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return post


# @router.delete("/{id}", response_model=schemas.Post)
# def delete_post(*, db: Session = Depends(deps.get_db), id: int) -> Any:
#     """
#     Delete an post.
#     """
#     post = crud.post.get(db=db, id=id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     post = crud.post.remove(db=db, id=id)
#     return post
