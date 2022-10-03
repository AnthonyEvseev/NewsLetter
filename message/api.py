from fastapi import APIRouter
from enum import Enum

message_router = APIRouter()


@message_router.get('/message', summary="Get information about message")
async def get_user():
    return 'get работает'


@message_router.post('/message', summary="Create a message")
async def post_user():
    return 'post работает'


@message_router.put('/message', summary="Put information about message")
async def put_user():
    return 'put работает'


@message_router.delete('/message', summary="Delete information about message")
async def delete_user():
    return 'delete работает'
