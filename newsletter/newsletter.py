import asyncio
import time
from datetime import datetime

from fastapi import Depends
import aiohttp
from core.config import URL_NEWSLETTERS, SECRET_TOKEN
from core.database import session, connect_db
from core.models import UserModel
from .schemas import NewsLetter
from celery import shared_task
import requests

header = {'Authorization': SECRET_TOKEN}


def found_user(code, tag, db: session = Depends(connect_db)):
    return db.query(UserModel).filter(UserModel.code == code).filter(UserModel.tags == tag).all()


# def create_user_data(schemas: NewsLetter, db: session = Depends(connect_db)):
#     user = found_user(schemas, db)
#     user_id = [number.id for number in user]
#     user_number = [number.phone_number for number in user]
#     user_data = {user_id: user_number for (user_id, user_number) in zip(user_id, user_number)}
#     return user_data

def create_user_data(code: str, tag: str, db: session = Depends(connect_db)):
    user = found_user(code, tag, db)
    user_id = [number.id for number in user]
    user_number = [number.phone_number for number in user]
    user_data = {user_id: user_number for (user_id, user_number) in zip(user_id, user_number)}
    return user_data


@shared_task()
def send(user_id, phone, text):
    datetime.now()
    time.sleep(10)
    requests.post(f'{URL_NEWSLETTERS}{user_id}', headers=header, json={
        'id': user_id,
        'phone': phone,
        'text': text,
    })


# _________________________________________________________
def send_messages(code: str, tag: str, text: str, db: session = Depends(connect_db)):
    user_data = create_user_data(code, tag, db)
    req = []
    for user_id, phone in user_data.items():
        req.append(send.delay(user_id, phone, text))



# def send_messages(schemas: NewsLetter, db: session = Depends(connect_db)):
#     user_data = create_user_data(schemas, db)
#     _req = []
#     for user_id, phone in user_data.items():
#         requests.post(f'{URL_NEWSLETTERS}{user_id}', headers=header, json={
#             'id': user_id,
#             'phone': 79286364850,
#             'text': schemas.text,
#         })

# def finally_send_message(id, ):
#
#     for user_id, phone in user.items():
#         requests.post(f'https://probe.fbrq.cloud/v1/send/1', headers=header, json={
#             'id': 1,
#             'phone': 79286364850,
#             'text': 'schemas',
#         })
#
#
# def dump(schemas: NewsLetter, db: session = Depends(connect_db)):
#     user_data = create_user_data(schemas, db)
#     test = schemas.text
#     for


# async def send_messages(code: int, tag: str, text: str, db: session = Depends(connect_db)):
#     user_data = create_user_data(schemas, db)
#     responses = []
#     async with aiohttp.ClientSession() as session_aiohttp:
#         for user_id, number in enumerate(user_data):
#             async with session_aiohttp.post(f'{URL_NEWSLETTERS}{user_id}', headers=header, json={
#                 'id': user_id,
#                 'phone': number,
#                 'text': schemas.text,
#             }) as resp:
#                 responses.append(await resp.json())
#     return responses
