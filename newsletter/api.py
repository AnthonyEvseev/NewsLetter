from datetime import time, datetime, date
from fastapi import APIRouter, Depends, Query
from core.config import SECRET_TOKEN
from core.database import session, connect_db
from newsletter.newsletter import create_task

newsletter_router = APIRouter()

header = {'Authorization': SECRET_TOKEN}


@newsletter_router.get('/message_1', summary="message_1")
async def message():
    return datetime.now()


@newsletter_router.get('/send_message', summary="send_message")
async def send_message(text: str, date_start: date, time_start: time, date_stop: date, time_stop: time, tag: str,
                       code: str = Query(max_length=3),
                       db: session = Depends(connect_db)):

    _date_start = datetime(date_start.year, date_start.month, date_start.day, time_start.hour, time_start.minute,
                           time_start.second)

    _date_stop = datetime(date_stop.year, date_stop.month, date_stop.day, time_stop.hour, time_stop.minute,
                          time_stop.second)

    if _date_start <= datetime.now() <= _date_stop:
        timer_start = 0
        return create_task(timer_start, text, tag, code, db)
    else:
        delta_seconds = _date_start - datetime.now()
        timer_start = delta_seconds.seconds
        return create_task(timer_start, text, tag, code, db)
