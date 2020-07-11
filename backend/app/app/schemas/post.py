from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class PostBase(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    created: Optional[datetime] = None


# Properties to receive on post creation
class PostCreate(PostBase):
    title: str
    url: str


# Properties to receive on post update
class PostUpdate(PostBase):
    pass


# Properties shared by models stored in DB
class PostInDBBase(PostBase):
    id: int
    title: str
    url: str
    created: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Post(PostInDBBase):
    pass


# Properties properties stored in DB
class PostInDB(PostInDBBase):
    pass


PostColumns = Enum("PostColumns", {field: field for field in Post.__fields__.keys()})
