from fastapi import Depends, Query
from celery import shared_task
import datetime
import requests
import time
from core.config import URL_NEWSLETTERS, HEADER
from core.database import session, connect_db
from core.models import UserModel
from message.crud import create_message
from celery.result import AsyncResult


def found_user(tag: str, code: str = Query(max_length=50), db: session = Depends(connect_db)):
    user = db.query(UserModel).filter(UserModel.code == code).filter(UserModel.tags == tag).all()
    if user:
        return user
    else:
        raise {'response 404': 'Клиент не найден'}


def create_user_data(tag: str, code: str = Query(max_length=50), db: session = Depends(connect_db)):
    user = found_user(tag, code, db)
    user_id = [number.id for number in user]
    user_number = [number.phone_number for number in user]
    user_data = {user_id: user_number for (user_id, user_number) in zip(user_id, user_number)}
    return user_data


@shared_task()
def send_messages(time_start, user_id, phone, text):
    try:
        time.sleep(time_start)
        res = requests.post(f'{URL_NEWSLETTERS}{user_id}', headers=HEADER, json={
            'id': user_id,
            'phone': phone,
            'text': text,
        })
        return {'response 200': res.json()}
    except:
        raise {'response 400': 'Ошибка внешнего сервиса'}


def create_task(id_news: int, delta_time: datetime, text: str, tag: str, code: str = Query(max_length=3),
                db: session = Depends(connect_db)):
    try:
        user_data = create_user_data(tag, code, db)
        for user_id, phone in user_data.items():
            task = send_messages.delay(delta_time.seconds, user_id, phone, text)
            time_start = delta_time + datetime.datetime.now()
            status_task = AsyncResult(task.id)
            status = str(status_task.status)
            create_message(id_news, time_start, task.id, status, user_id, db)
    except:
        raise {'response 404': 'Клиент не найден'}
