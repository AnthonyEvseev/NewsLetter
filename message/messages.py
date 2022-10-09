from celery.result import AsyncResult
from newsletter.newsletter import send_messages
from celery import current_task


