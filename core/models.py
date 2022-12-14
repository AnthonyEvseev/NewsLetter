from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey

Base = declarative_base()


class NewsletterModel(Base):
    __tablename__ = 'newsletter'

    id = Column(Integer(), primary_key=True)
    text = Column(String(300))
    date_start = Column(Date())
    date_stop = Column(Date())
    code = Column(String)
    tags = Column(String)

    message = relationship('MessageModel', back_populates='newsletter')


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    phone_number = Column(String(11), unique=True)
    code = Column(String)
    tags = Column(String)
    time_zone = Column(String())

    message = relationship('MessageModel', back_populates='user')


class MessageModel(Base):
    __tablename__ = 'message'

    id = Column(Integer(), primary_key=True)
    id_celery = Column(String)
    date_send = Column(DateTime)
    status_send = Column(String)

    id_newsletter = Column(Integer, ForeignKey('newsletter.id'))
    id_user = Column(Integer, ForeignKey('user.id'))

    newsletter = relationship('NewsletterModel', back_populates='message')
    user = relationship('UserModel', back_populates='message')
