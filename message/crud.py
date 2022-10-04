# from fastapi import Depends
# from core.database import session, connect_db
# from core.models import UserModel
# from .schemas import UserSchemas, UserIDSchemas
#
#
# def get_user(db: session):
#     return db.query(UserModel).all()
#
#
# def get_user_by_id(schemas: UserIDSchemas, db: session = Depends(connect_db)):
#     return db.query(UserModel).filter(UserModel.id == schemas.id).first()
#
#
# def create_user(schemas: UserSchemas, db: session = Depends(connect_db)):
#     try:
#         _user = UserModel(phone_number=schemas.phone_number, tags=schemas.tags, code=schemas.phone_number[1:4],
#                           time_zone=schemas.time_zone)
#         db.add(_user)
#         db.commit()
#         db.refresh(_user)
#         return _user
#     except:
#         raise {'resource': 400}
#
#
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
