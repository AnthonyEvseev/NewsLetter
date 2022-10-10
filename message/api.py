from fastapi import APIRouter, HTTPException, status, Response, Depends
from core.database import session, connect_db
from message.crud import get_message, message_group, message_status

message_router = APIRouter()


@message_router.get('/all_message', summary="all_message")
async def get_info(db: session = Depends(connect_db)):
    """
            Инструкция:

            - Выводит все созданные сообщения. Информация о статусе не актуальна (можно потом переделать)
    """
    return get_message(db)


@message_router.get('/message_by_group', summary="message_by_group")
async def post_user(id_news: int, db: session = Depends(connect_db)):
    """
            Инструкция:

            - **ID** Выводит сообщения по определённой рассылке.
            Информация о статусе не актуальна (можно потом переделать)
    """
    return message_group(id_news, db)


@message_router.get('/message_by_status', summary="message_by_status")
async def post_user(status_news: str, db: session = Depends(connect_db)):
    """
            Инструкция:

            - **STATUS** Выводит сообщения по определённому статусу.
            Информация о статусе не актуальна (можно потом переделать)
    """
    return message_status(status_news, db)
