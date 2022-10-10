from celery import shared_task
from celery.result import AsyncResult
from fastapi import Depends
from datetime import date
from core.database import session, connect_db
from core.models import NewsletterModel, MessageModel


def get_all_newsletter(db: session = Depends(connect_db)):
    return db.query(NewsletterModel).all()


def get_one_newsletter(id_news: int, db: session = Depends(connect_db)):
    return db.query(NewsletterModel).filter(NewsletterModel.id == id_news).first()


def list_tasks(id_news: int, db: session = Depends(connect_db)):
    return db.query(MessageModel.id_celery).filter(MessageModel.id_newsletter == id_news).all()


@shared_task()
def revoke_tasks(id_task):
    task = AsyncResult(id=id_task)
    task.revoke(terminate=True)


def delete_tasks(id_news: int, db: session = Depends(connect_db)):
    list_t = list_tasks(id_news, db)
    for i in list_t:
        revoke_tasks.delay(i.id_celery)


def create_newsletter_db(id_news: int, date_start: date, date_stop: date, text, tag, code,
                         db: session = Depends(connect_db)):
    try:
        newsletter = NewsletterModel(id=id_news, date_start=date_start, date_stop=date_stop, text=text, tags=tag,
                                     code=code)
        db.add(newsletter)
        db.commit()
        db.refresh(newsletter)
        return newsletter
    except:
        return {'resource': 400}


def remove_newsletter(id_news: int, db: session = Depends(connect_db)):
    try:
        delete_tasks(id_news, db)
        _user = get_one_newsletter(id_news, db)
        db.delete(_user)
        db.commit()
    except:
        return {'resource': 400}
