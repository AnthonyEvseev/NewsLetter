import time
from fastapi import Depends, Query
from core.config import URL_NEWSLETTERS, SECRET_TOKEN
from core.database import session, connect_db
from core.models import UserModel
from celery import shared_task
import requests

header = {'Authorization': SECRET_TOKEN}


def found_user(tag, code, db: session = Depends(connect_db)):
    return db.query(UserModel).filter(UserModel.code == code).filter(UserModel.tags == tag).all()


def create_user_data(tag: str, code: str = Query(max_length=50), db: session = Depends(connect_db)):
    user = found_user(tag, code, db)
    user_id = [number.id for number in user]
    user_number = [number.phone_number for number in user]
    user_data = {user_id: user_number for (user_id, user_number) in zip(user_id, user_number)}
    return user_data


@shared_task()
def send(user_id, phone, text):
    time.sleep(5)
    res = requests.post(f'{URL_NEWSLETTERS}{user_id}', headers=header, json={
        'id': user_id,
        'phone': phone,
        'text': text,
    })
    return {'response': res.json()}


def send_messages(text: str, tag: str, code: str = Query(max_length=3), db: session = Depends(connect_db)):
    user_data = create_user_data(tag, code, db)
    res = []
    for user_id, phone in user_data.items():
        res.append(send.delay(user_id, phone, text))
