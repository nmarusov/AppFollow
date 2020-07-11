import re
from datetime import datetime

import requests
from sqlalchemy.exc import InvalidRequestError

from app.core.celery_app import celery_app
from app import crud
from app.db.session import SessionLocal
from app.models.post import Post


URL = "https://news.ycombinator.com/news"
PATTERN = re.compile(
    r'<a href=\"(?P<url>.+?)\" class="storylink"(?: rel="nofollow")?>(?P<title>.+?)</a>'
)
MAX_POSTS = 30


@celery_app.task(acks_late=True)
def parse_page(url: str) -> str:
    content = requests.get(url).text
    matches = PATTERN.finditer(content)
    items = [match.groupdict() for match in matches][:MAX_POSTS]
    session = SessionLocal()
    count = 0
    msg = ""

    for item in items:
        try:
            post = crud.post.create(db=session, obj_in=item)
            count += 1
        except Exception:
            pass

    return f"{count}/{len(items)} posts added"
