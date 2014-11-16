# coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__author__ = 'o.pasichnyk'
__all__ = ['PostgreSqlConnect', ]


class _Singleton(object):
    '''Class that realize singleton pattern'''
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)

        return class_._instance


class PostgreSqlConnect(_Singleton):
    '''Connect to PostgreSQL server using sqlalchemy'''
    engine = None #sqlalchemy engine tool
    session = None #sqlalchemy seesin tool

    def __init__(self, db_settings={}, debug=False):
        '''
        :param db_settings: dict - conntect settings
        :param debug: bool - True to show debug info, otherwise False
        :return: None
        '''
        Base = declarative_base()

        self.engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{name}'.format(**db_settings))
        self.engine.echo = debug

        session = sessionmaker(self.engine)
        self.session = session()
        Base.metadata.create_all(self.engine)
