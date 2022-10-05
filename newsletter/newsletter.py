from fastapi import Depends
import aiohttp
from crontab import CronTab
from datetime import datetime
from core.config import URL_NEWSLETTERS, SECRET_TOKEN
from core.database import session, connect_db
from core.models import UserModel
from .schemas import NewsLetter

header = {'Authorization': SECRET_TOKEN}


def found_user(schemas: NewsLetter, db: session = Depends(connect_db)):
    return db.query(UserModel).filter(UserModel.tags == schemas.tags).filter(UserModel.code == schemas.code).all()


def create_user_data(schemas: NewsLetter, db: session = Depends(connect_db)):
    user = found_user(schemas, db)
    user_id = [number.id for number in user]
    user_number = [number.phone_number for number in user]
    user_data = {user_id: user_number for (user_id, user_number) in zip(user_id, user_number)}
    return user_data


async def send_messages(schemas: NewsLetter, db: session = Depends(connect_db)):
    user_data = create_user_data(schemas, db)
    responses = []
    async with aiohttp.ClientSession() as session_aiohttp:
        for user_id, number in enumerate(user_data):
            async with session_aiohttp.post(f'{URL_NEWSLETTERS}{user_id}', headers=header, json={
                'id': user_id,
                'phone': number,
                'text': schemas.text,
            }) as resp:
                responses.append(await resp.json())
    return responses


def timer123(schemas: NewsLetter, db: session = Depends(connect_db)):
    cron = CronTab(user='root')
    job = cron.new(send_messages(schemas, db))

    year = schemas.date_start.year
    month = schemas.date_start.month
    day = schemas.date_start.day
    hour = schemas.date_start.hour
    minutes = schemas.date_start.minute

    job.setall(datetime(year, month, day, hour, minutes))
