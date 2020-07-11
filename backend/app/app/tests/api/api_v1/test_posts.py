from datetime import datetime
from operator import attrgetter
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from sqlalchemy import create_engine

from app.core.config import settings
from app.tests.utils.post import create_random_post
from app.models import Post

import pytest


def setup_function(function):
    db = SessionLocal()
    db.query(Post).delete()
    db.commit()


def test_get_posts_by_id(client: TestClient, db: Session) -> None:
    NUM_POSTS = 3
    posts = [create_random_post(db) for _ in range(NUM_POSTS)]
    response = client.get(f"{settings.API_V1_STR}/posts")

    assert response.status_code == 200

    content = response.json()
    assert isinstance(content, list)
    assert len(content) == NUM_POSTS

    for i, post in enumerate(posts):
        assert content[i]["title"] == post.title
        assert content[i]["url"] == post.url
        assert content[i]["id"] == post.id
        assert datetime.fromisoformat(content[i]["created"]) == post.created


@pytest.mark.parametrize("order", ("id", "title", "url", "created"))
@pytest.mark.parametrize("direction", ("asc", "desc"))
def test_get_posts(client: TestClient, db: Session, order, direction) -> None:
    NUM_POSTS = 10

    posts = [create_random_post(db) for _ in range(NUM_POSTS)]

    params = {"order": order, "direction": direction, "limit": NUM_POSTS}
    response = client.get(f"{settings.API_V1_STR}/posts", params=params)

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)
    assert len(content) == NUM_POSTS

    for i, post in enumerate(
        sorted(posts, key=attrgetter(order), reverse=(direction == "desc"))
    ):
        if isinstance(getattr(post, order), datetime):
            assert datetime.fromisoformat(content[i][order]) == getattr(post, order)
        else:
            assert content[i][order] == getattr(post, order)


@pytest.mark.parametrize("limit", (5, 10, 15))
def test_get_posts_limit(client: TestClient, db: Session, limit) -> None:
    NUM_POSTS = 10

    posts = [create_random_post(db) for _ in range(NUM_POSTS)]

    params = {"limit": limit}
    response = client.get(f"{settings.API_V1_STR}/posts", params=params)

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)
    assert len(content) == min(limit, NUM_POSTS)


@pytest.mark.parametrize("limit", (-1, 0, 101))
def test_get_posts_limit_margins(client: TestClient, db: Session, limit) -> None:
    params = {"limit": limit}
    response = client.get(f"{settings.API_V1_STR}/posts", params=params)

    assert response.status_code != 200

    content = response.json()

    assert isinstance(content, dict)
    assert content["detail"][0]["type"].startswith("value_error.number")


def test_get_posts_limit_default(client: TestClient, db: Session) -> None:
    DEFAULT_LIMIT = 5
    NUM_POSTS = 10

    posts = [create_random_post(db) for _ in range(NUM_POSTS)]

    response = client.get(f"{settings.API_V1_STR}/posts")

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)
    assert len(content) == DEFAULT_LIMIT


@pytest.mark.parametrize("offset", (0, 5, 10, 15))
def test_get_posts_offset(client: TestClient, db: Session, offset) -> None:
    NUM_POSTS = 10

    posts = [create_random_post(db) for _ in range(NUM_POSTS)]

    params = {"offset": offset, "limit": 20}
    response = client.get(f"{settings.API_V1_STR}/posts", params=params)

    assert response.status_code == 200

    content = response.json()

    assert isinstance(content, list)
    assert len(content) == max(0, NUM_POSTS - offset)


@pytest.mark.parametrize("offset", (-1,))
def test_get_posts_offset_margins(client: TestClient, db: Session, offset) -> None:
    params = {"offset": offset, "limit": 20}
    response = client.get(f"{settings.API_V1_STR}/posts", params=params)

    assert response.status_code != 200

    content = response.json()

    assert isinstance(content, dict)
    assert content["detail"][0]["type"].startswith("value_error.number")
