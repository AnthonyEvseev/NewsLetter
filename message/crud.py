from celery.result import AsyncResult
from fastapi import Depends
from typing import Any
from datetime import datetime
from core.database import session, connect_db
from core.models import MessageModel
from user.message import update_status


def get_message(db: session):
    return db.query(MessageModel).all()


# def status_message(id_task, db: session = Depends(connect_db)):
#     return db.query(MessageModel).all(MessageModel.id_celery == id_task).first()


# def rebase_status(id_task, db):
#     return db.query(MessageModel).all(MessageModel.id_celery == id_task).first()


# def create_new_status(id_task, status, db):
#     message = rebase_status(id_task, db)
#     message.status_send = status
#     db.commit()
#     db.refresh(message)
#
#
# def check_status_message(db: session = Depends(connect_db)):
#     all_messages = get_message(db)
#     for i in all_messages:
#         id_task = i.id_celery
#         status_task = AsyncResult(id_task)
#         status = status_task.status
#         create_new_status(id_task, status, db)


def create_message(id_news: int, time_start: datetime, task_id: str, status: str, user_id: int,
                   db: session = Depends(connect_db)):
    try:
        user = MessageModel(id_newsletter=id_news, date_send=time_start, id_celery=task_id,
                            id_user=user_id, status_send=status)
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        raise {'resource': 400}


def message_group(id_news: int, db: session = Depends(connect_db)):
    return db.query(MessageModel).filter(MessageModel.id_newsletter == id_news).all()


def message_status(status_news: str, db: session = Depends(connect_db)):
    return db.query(MessageModel).filter(MessageModel.status_send == status_news).all()
