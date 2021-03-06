from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.base_class import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    url = Column(String, index=True)
    created = Column(DateTime(timezone=True), default=func.now())
