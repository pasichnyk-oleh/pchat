# coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from sqlalchemy.orm.exc import NoResultFound

from db_connect import db
from models.base import Base
from models.field_handlers import model_field_proccesing, Md5Handler

__author__ = 'o.pasichnyk'
__all__ = ['User', ]


class User(Base):
    __tablename__ = 'users'

    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    @staticmethod
    def isset_user(name, password):
        '''
        Check exist or not user in DB

        :param password: str - user name
        :param string: str - user password
        : return: dict - {} if not isset or dict with user_name and user_id keys
        '''
        md5_password = Md5Handler().process(password)

        try:
            user = db.query(User).filter_by(name=name, password=md5_password).one()
        except NoResultFound:
            return {}
        else:
            return {'user_name': name, 'user_id': user.id}

    @validates('password')
    @model_field_proccesing(Md5Handler())
    def validate_password(self, key, password):
        return password
