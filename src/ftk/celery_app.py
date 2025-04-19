from celery import Celery
from celery.schedules import crontab


celery = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery.conf.timezone = "UTC"
celery.autodiscover_tasks(['src.ftk'])

celery.conf.beat_schedule = {
    "run-parser-weekly": {
        "task": "src.ftk.tasks.call_ftk_parser_endpoint",
        "schedule": crontab(minute="*/5")
    }
}