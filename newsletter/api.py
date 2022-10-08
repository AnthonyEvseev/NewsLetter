from datetime import time, datetime, timedelta, date
from fastapi import APIRouter, Depends, Query
from core.config import SECRET_TOKEN
from core.database import session, connect_db
from newsletter.newsletter import create_task

# from newsletter.newsletter import create_task

newsletter_router = APIRouter()

header = {'Authorization': SECRET_TOKEN}


@newsletter_router.get('/message_1', summary="message_1")
async def message():
    return datetime.now()


@newsletter_router.get('/send_message', summary="send_message")
async def send_message(text: str, date_start: date, time_start: time, date_stop: date, time_stop: time, tag: str,
                       code: str = Query(max_length=3),
                       db: session = Depends(connect_db)):
    # if time_start <= datetime.time(datetime.now()) <= time_stop:
    #     return create_task(text, tag, code, db)
    # else:

    _date = datetime(date_start.year, date_start.month, date_start.day, time_start.hour, time_start.minute,
                     time_start.second)

    a = _date - datetime.now()
    b = a.seconds
    return create_task(b, text, tag, code, db)
