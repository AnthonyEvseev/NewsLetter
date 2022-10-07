import uvicorn
from celery import Celery
from fastapi import FastAPI
from core.config import ROUT, PORT, CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from user.api import user_router
from newsletter.api import newsletter_router
from message.api import message_router

app = FastAPI()

app.include_router(user_router, tags=["User"])
app.include_router(newsletter_router, tags=["Newsletter"])
app.include_router(message_router, tags=["Message"])

celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.imports = [
    'newsletter.celery',
    'newsletter.newsletter'

]

if __name__ == '__main__':
    uvicorn.run(ROUT, port=PORT, reload=True)
