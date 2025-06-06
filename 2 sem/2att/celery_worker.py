from celery import Celery
import os

celery = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    enable_utc=True
)