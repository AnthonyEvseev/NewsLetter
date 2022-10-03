from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, DateTime, BOOLEAN, ForeignKey

Base = declarative_base()


# class CodeModel(Base):
#     __tablename__ = 'code_model'
#
#     id = Column(Integer(), primary_key=True)
#     name = Column(String())
#
#     newsletter = relationship('Newsletter', back_populates='code_model')
#     user = relationship('User', back_populates='code_model')


# class TagsModel(Base):
#     __tablename__ = 'tags'
#
#     id = Column(Integer(), primary_key=True)
#     name = Column(String())
#
#     newsletter = relationship('Newsletter', back_populates='tags')
#     user = relationship('User', back_populates='tags')


class Newsletter(Base):
    __tablename__ = 'newsletter'

    id = Column(Integer(), primary_key=True)

    # id_code = Column(Integer, ForeignKey('code_model.id'))
    # tag = Column(Integer, ForeignKey('tags.id'))

    text = Column(String(300))
    date_start = Column(DateTime())
    date_stop = Column(DateTime())

    code = Column(String)
    tags = Column(String)
    # code = relationship('CodeModel', back_populates='newsletter')
    # tags_model = relationship('TagsModel', back_populates='newsletter')
    message = relationship('Message', back_populates='newsletter')


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    phone_number = Column(String(11), unique=True)
    code = Column(String)
    tags = Column(String)

    # operator_code = Column(Integer, ForeignKey('code_model.id'))
    # tag = Column(Integer, ForeignKey('tags.id'))

    time_zone = Column(String())

    message = relationship('Message', back_populates='user')
    # code = relationship('Newsletter', back_populates='user')
    # tag_model = relationship('TagsModel', back_populates='user')


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer(), primary_key=True)
    date_send = Column(DateTime())
    status_send = Column(BOOLEAN)

    id_newsletter = Column(Integer, ForeignKey('newsletter.id'))
    id_user = Column(Integer, ForeignKey('user.id'))

    newsletter = relationship('Newsletter', back_populates='message')
    user = relationship('UserModel', back_populates='message')
