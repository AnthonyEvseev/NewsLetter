import asyncio
import aiohttp
from fastapi import APIRouter, Response, Depends
from core.config import SECRET_TOKEN
from core.database import session, connect_db
from core.models import UserModel
from newsletter.crud import get_history
from newsletter.newsletter import message, found_user
from newsletter.schemas import NewsLetter
import requests

newsletter_router = APIRouter()

header = {'Authorization': SECRET_TOKEN}


# url = 'https://probe.fbrq.cloud/v1/send/1'


@newsletter_router.get('/test', summary="test")
async def test():
    site = 'https://probe.fbrq.cloud/v1/send/1'
    a = requests.post(site, headers=header, json={

        "id": 1,
        "phone": 79064780272,
        "text": "test"

    })

    return str(a)


@newsletter_router.post('/test2', summary="test2")
async def get_newsletter_test(schemas: NewsLetter, db: session = Depends(connect_db)):
    async with aiohttp.ClientSession() as session_aiohttp:
        task = message(schemas, session_aiohttp, db)
        # await asyncio.gather(*task)


@newsletter_router.get('/newsletter', summary="Newsletter history")
async def get_newsletter(db: session = Depends(connect_db)):
    return get_history(db)

# @newsletter_router.post('/newsletter', summary="Create a newsletter")
# async def post_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
#     return message(schemas, db)
# try:
#     create_newsletter(schemas, db)
#     # test = found_user(schemas, db)
#     test = message(schemas, db)
#     response.status_code = status.HTTP_200_OK
#     return 'post работает', test
# except:
#     raise HTTPException(status_code=400, detail='Упало (')


# @newsletter_router.put('/newsletter', summary="Put information about newsletters")
# async def put_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
#     return 'put работает'
#
#
# @newsletter_router.delete('/newsletter', summary="Delete information about newsletters")
# async def delete_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
#     return 'delete работает'
