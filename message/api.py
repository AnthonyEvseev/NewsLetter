from fastapi import APIRouter, HTTPException, status, Response, Depends
from core.database import session, connect_db
from enum import Enum

from message.crud import get_message

message_router = APIRouter()


@message_router.get('/all_message', summary="all_message")
async def get_info(db: session = Depends(connect_db)):
    return get_message(db)


@message_router.post('/message', summary="Create a message")
async def post_user():
    return 'post работает'


@message_router.put('/message', summary="Put information about message")
async def put_user():
    return 'put работает'


@message_router.delete('/message', summary="Delete information about message")
async def delete_user():
    return 'delete работает'
