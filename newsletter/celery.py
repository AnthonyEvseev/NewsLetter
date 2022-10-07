import asyncio
import time

from celery import shared_task


@shared_task()
def divide(x, y):
    # time.sleep(15)
    return x / y
