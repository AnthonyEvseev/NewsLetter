from fastapi import APIRouter, Depends

from core.config import SECRET_TOKEN
from core.database import session, connect_db
from newsletter.newsletter import create_user_data, found_user, send_messages
from newsletter.schemas import NewsLetter
from newsletter.celery import divide
import requests

newsletter_router = APIRouter()

header = {'Authorization': SECRET_TOKEN}


@newsletter_router.post('/test', summary="test")
async def test():
    divide.delay(10, 5)


@newsletter_router.get('/send_message', summary="test")
async def send_message_test(code: str, tag: str, text: str, db: session = Depends(connect_db)):
    # return send_messages(code, tag, text, db)
    return send_messages(code, tag, text, db)

# @newsletter_router.post('/send_message21231', summary="test1321")
# async def send_message_test2(schemas: NewsLetter, db: session = Depends(connect_db)):
#     return create_user_data(schemas, db)

# r = requests.post('https://probe.fbrq.cloud/v1/send/1', headers=header, json={
#     'id': 1,
#     'phone': 79286364850,
#     'text': 'message',
# })
# return str(r)

# @newsletter_router.post('/send_message', summary="send_message")
# async def send_message_test(schemas: NewsLetter, db: session = Depends(connect_db)):
#     text_message = schemas.text
#     data = create_user_data(schemas, db)
#     # return await send_messages(text_message, data)
#     send_messages.delay(text_message, data)
#     return 'ok'
