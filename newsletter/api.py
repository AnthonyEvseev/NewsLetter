from fastapi import APIRouter, Depends
from core.database import session, connect_db
from newsletter.celery import divide
from newsletter.crud import get_history
from newsletter.newsletter import send_messages
from newsletter.schemas import NewsLetter
from celery import shared_task

newsletter_router = APIRouter()


@newsletter_router.post('/test', summary="test")
async def test():
    divide.delay(10, 5)


@newsletter_router.post('/send_message', summary="send_message")
async def test(schemas: NewsLetter, db: session = Depends(connect_db)):
    return await send_messages(schemas, db)


@newsletter_router.get('/newsletter', summary="Newsletter history")
async def get_newsletter(db: session = Depends(connect_db)):
    return get_history(db)

# @newsletter_router.put('/newsletter', summary="Put information about newsletters")
# async def put_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
#     return 'put работает'
#
#
# @newsletter_router.delete('/newsletter', summary="Delete information about newsletters")
# async def delete_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
#     return 'delete работает'
