from fastapi import APIRouter, HTTPException, status, Response, Depends
from core.database import session, connect_db

from message.crud import get_message, message_group, message_status

message_router = APIRouter()


@message_router.get('/all_message', summary="all_message")
async def get_info(db: session = Depends(connect_db)):
    return get_message(db)


@message_router.get('/message_by_group', summary="message_by_group")
async def post_user(id_news: int, db: session = Depends(connect_db)):
    return message_group(id_news, db)


@message_router.get('/message_by_status', summary="message_by_status")
async def post_user(status_news: str, db: session = Depends(connect_db)):
    return message_status(status_news, db)


# @message_router.get('/status', summary="status")
# def all_newsletter(db: session = Depends(connect_db)):
#     return check_status_message(db)
