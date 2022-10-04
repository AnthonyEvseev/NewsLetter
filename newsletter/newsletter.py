from fastapi import Depends
from core.database import session, connect_db
from core.models import UserModel
from .schemas import NewsLetter
import asyncio

url = 'https://probe.fbrq.cloud/v1/send/1'
url2 = 'https://vk.com/'


def found_user(schemas: NewsLetter, db: session = Depends(connect_db)):
    return db.query(UserModel).filter(UserModel.tags == schemas.tags).filter(UserModel.code == schemas.code).all()


def send_message(schemas: NewsLetter, session_aiohttp, db: session = Depends(connect_db)):
    users = found_user(schemas, db)
    task = []
    for number in users:
        task.append(asyncio.create_task(session_aiohttp.get(url, json={
            "id": schemas.id,
            "phone": number.phone_number,
            "text": schemas.text
        })))
    return task
