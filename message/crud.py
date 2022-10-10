from fastapi import Depends
from datetime import datetime
from core.database import session, connect_db
from core.models import MessageModel


def get_message(db: session):
    return db.query(MessageModel).all()


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
