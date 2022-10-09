from datetime import time, datetime, date, timedelta
from fastapi import APIRouter, Depends, Query
from core.database import session, connect_db
from newsletter.newsletter import create_task, found_user
from newsletter.crud import create_newsletter_db

newsletter_router = APIRouter()


# @newsletter_router.get('/test', summary="send_message")
# async def create_newslett123er(text: str, date_start: date, time_start: time, date_stop: date, time_stop: time,
#                                tag: str,
#                                code: str = Query(max_length=3),
#                                db: session = Depends(connect_db)):
#     return found_user(tag, code, db)


@newsletter_router.get('/send_message', summary="send_message")
async def create_newsletter(id_news: int, text: str, date_start: date, time_start: time, date_stop: date,
                            time_stop: time, tag: str,
                            code: str = Query(max_length=3),
                            db: session = Depends(connect_db)):
    _date_start = datetime(date_start.year, date_start.month, date_start.day, time_start.hour, time_start.minute,
                           time_start.second)

    _date_stop = datetime(date_stop.year, date_stop.month, date_stop.day, time_stop.hour, time_stop.minute,
                          time_stop.second)

    if _date_start <= datetime.now() <= _date_stop:
        timer_start = timedelta(seconds=1)
        try:
            create_newsletter_db(id_news, _date_start, _date_stop, text, tag, code, db)
            create_task(id_news, timer_start, text, tag, code, db)
            return {'response 200': 'Рассылка отправлена'}
        except:
            return {'response 404': 'Клиент не найден'}
    if _date_stop <= datetime.now() <= _date_start:
        return {'response 400': 'Вы ввели недопустимый интервал времени'}
    else:
        try:
            delta_seconds = _date_start - datetime.now()
            create_newsletter_db(id_news, _date_start, _date_stop, text, tag, code, db)
            create_task(id_news, delta_seconds, text, tag, code, db)
            return {'response 200': f'Рассылка будет запущена {_date_start}'}
        except:
            return {'response 400': 'ID рассылки уже существует'}
