from src.config.celery import app


@app.task
def refresh_feed(url):
    print("dummy celery task")