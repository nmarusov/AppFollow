from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str,
        direction: str
    ) -> List[Post]:
        if order_by not in Post.__table__.columns.keys():
            return self.get_multi(db, skip=skip, limit=limit)
        else:
            return (
                db.query(self.model)
                .order_by(getattr(getattr(Post, order_by), direction)())
                .offset(skip)
                .limit(limit)
                .all()
            )


post = CRUDPost(Post)
