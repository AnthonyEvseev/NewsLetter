from fastapi import APIRouter
from enum import Enum

newsletter_router = APIRouter()


@newsletter_router.get('/newsletter', summary="Get information about newsletters")
async def get_user():
    return 'get работает'


@newsletter_router.post('/newsletter', summary="Create a newsletter")
async def post_user():
    return 'post работает'


@newsletter_router.put('/newsletter', summary="Put information about newsletters")
async def put_user():
    return 'put работает'


@newsletter_router.delete('/newsletter', summary="Delete information about newsletters")
async def delete_user():
    return 'delete работает'
