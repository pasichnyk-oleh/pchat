# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['Chat', 'ChatUser', 'Message', ]

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import validates

import settings
from models.base import Base
from db_connect import db
from models.field_handlers import model_field_proccesing, ImageFindHandler


class Chat(Base):
    __tablename__ = 'chats'

    user_id = Column('user_id', Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(20), nullable=False)


class ChatUser(Base):
    __tablename__ = 'chats_user'

    chat_id = Column('chat_id', Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column('user_id', Integer, ForeignKey("users.id"), nullable=False)

    @classmethod
    def get_user_chats(cls, user_id):
        '''
        Get id of chats that user join

        :param user_id: id of user to get chats
        :return: list of chats id
        '''
        user_in_chat = db.query(cls.chat_id).filter(cls.user_id == user_id).all()

        return [item.chat_id for item in user_in_chat]

    @classmethod
    def join_switcher(cls, user_id, chat_id):
        '''
        Switch user joining in some chat. If user is already joined - unjoin him, if not - join

        :param user_id: id of user to switch
        :param chat_id: id of chat to switch in
        :return: None
        '''
        try:
            row = db.query(ChatUser).filter(cls.chat_id==chat_id, cls.user_id==user_id).one()
        except NoResultFound:
            row = cls(user_id=user_id, chat_id=chat_id)
            db.add(row)
        else:
            db.delete(row)

        db.commit()

    @classmethod
    def has_access(cls, user_id, chat_id):
        '''
        Check if user has access to some chat

        :param user_id: id of user to check
        :param chat_id: id of chat to check
        :return: True if user have access or False if not have
        '''
        try:
            db.query(cls.id).filter(cls.user_id == user_id, cls.chat_id == chat_id).one()
        except NoResultFound:
            return False

        return True


class Message(Base):
    __tablename__ = 'messages'

    chat_id = Column('chat_id', Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column('user_id', Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)

    @validates('message')
    @model_field_proccesing(ImageFindHandler(settings.UPLOAD_FILES_ROOT))
    def validate_message(self, key, message):
        '''Validating message field'''
        return message
