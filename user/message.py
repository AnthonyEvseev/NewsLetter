from celery import shared_task
from celery.result import AsyncResult


@shared_task()
def update_status(id_task):
    status_task = AsyncResult(id_task)
    return status_task.status
