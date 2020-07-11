from celery import Celery
from app.core.config import settings

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.parse_page": "main-queue"}

celery_app.conf.beat_schedule = {
    "page-parsing-task": {
        "task": "app.worker.parse_page",
        "args": ("https://news.ycombinator.com/news",),
        "schedule": 300.0,
    }
}
