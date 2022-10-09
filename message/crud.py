from fastapi import Depends
from typing import Any
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

# def update_user(schemas: UserSchemas, db: session = Depends(connect_db)):
#     _user = get_user_by_id(schemas, db)
#     _user.phone_number = schemas.phone_number
#     _user.operator_code = schemas.phone_number[1:4]
#     _user.tags = schemas.tags
#     _user.time_zone = schemas.time_zone
#
#     db.commit()
#     db.refresh(_user)
#     return _user


# def remove_book(schemas, db: session = Depends(connect_db)):
#     _user = get_user_by_id(schemas, db)
#     db.delete(_user)
#     db.commit()
