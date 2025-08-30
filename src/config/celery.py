from celery import Celery
from os import environ

CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL")

app = Celery(
    'podalyze_celery', 
    broker=CELERY_BROKER_URL,
    include=["src.inference.tasks"],
    )