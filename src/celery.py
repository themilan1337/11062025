from celery import Celery
from celery.schedules import crontab

# This should ideally come from config, but for now, hardcoding for simplicity
REDIS_URL = "redis://localhost:6379/0"

celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.tasks.background_tasks"]  # Path to your tasks module
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
        'task': 'src.tasks.background_tasks.fetch_data_and_save_to_db',
        'schedule': crontab(hour=0, minute=0), # Everyday at midnight
    },
}

if __name__ == "__main__":
    celery_app.start()