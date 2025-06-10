from celery import Celery
from celery.schedules import crontab
from src.config import settings # Import settings from src.config

celery_app = Celery(
    "src.tasks", # Naming the app with src prefix for clarity
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["src.tasks.background_tasks"]  # Path to tasks module relative to PYTHONPATH
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Example of a periodic task: runs every day at midnight
celery_app.conf.beat_schedule = {
    'fetch-data-every-day': {
        'task': 'src.tasks.background_tasks.fetch_data_and_save_to_db', # Task path relative to PYTHONPATH
        'schedule': crontab(hour=0, minute=0), # Everyday at midnight
    },
}

if __name__ == "__main__":
    celery_app.start()