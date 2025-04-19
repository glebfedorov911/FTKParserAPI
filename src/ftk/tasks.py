import requests
from src.ftk.celery_app import celery


@celery.task
def call_ftk_parser_endpoint():
    try:
        response = requests.get("http://ftk_parser:8000/ftk/start_parser")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"failed: {e}")