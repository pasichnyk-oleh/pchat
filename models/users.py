# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['User', ]

from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from sqlalchemy.orm.exc import NoResultFound

from db_connect import db
from models.base import Base
from utils.md5_hash import decode_string
from models.field_handlers import model_field_proccesing, Md5Handler


class User(Base):
    __tablename__ = 'users'

    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    @staticmethod
    def isset_user(name, password):
        '''
        Check exist or not user in DB

        :param string: user name
        :param string: user password
        : return: None if not isset or dict with user_name and user_id keys
        '''
        md5_password = decode_string(password)

        try:
            user = db.query(User).filter_by(name=name, password=md5_password).one()
        except NoResultFound:
            return None
        else:
            return {'user_name': name, 'user_id': user.id}

    @validates('password')
    @model_field_proccesing(Md5Handler())
    def validate_password(self, key, password):
        return password
