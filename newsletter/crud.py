from fastapi import Depends
from core.database import session, connect_db
from core.models import NewsletterModel
from .schemas import NewsLetter


def get_history(db: session):
    return db.query(NewsletterModel).all()


# def create_history(schemas: NewsLetter, db: session = Depends(connect_db)):
#     return db.query(UserModel).filter(UserModel.id == schemas.id).first()

# def create_newsletter(time_start, db: session = Depends(connect_db)):
#     try:
#         newsletter = NewsletterModel(text=schemas.text, date_start=schemas.date_start, date_stop=schemas.date_stop,
#                                      code=schemas.code, tags=schemas.tags)
#         db.add(newsletter)
#         db.commit()
#         db.refresh(newsletter)
#         return newsletter
#     except:
#         raise {'resource': 400}

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
#
#
# def remove_book(schemas, db: session = Depends(connect_db)):
#     _user = get_user_by_id(schemas, db)
#     db.delete(_user)
#     db.commit()
