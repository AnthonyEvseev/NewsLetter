from fastapi import Depends, Query
from celery import shared_task
import datetime
import requests
import time
from core.config import URL_NEWSLETTERS, HEADER
from core.database import session, connect_db
from core.models import UserModel
from message.crud import create_message


def found_user(tag, code, db: session = Depends(connect_db)):
    try:
        return db.query(UserModel).filter(UserModel.code == code).filter(UserModel.tags == tag).all()
    except:
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


# def create_task(time_start, text: str, tag: str, code: str = Query(max_length=3), db: session = Depends(connect_db)):
#     user_data = create_user_data(tag, code, db)
#     for user_id, phone in user_data.items():
#         send_messages.delay(time_start, user_id, phone, text)

def create_task(delta_time, text: str, tag: str, code: str = Query(max_length=3), db: session = Depends(connect_db)):
    user_data = create_user_data(tag, code, db)
    for user_id, phone in user_data.items():
        task = send_messages.delay(delta_time.seconds, user_id, phone, text)
        time_start = delta_time + datetime.datetime.now()
        create_message(time_start, task.id, user_id)
