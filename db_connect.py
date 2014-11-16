# coding: utf-8 -*-
'''
Wrapping SQLAlchemy PostgreSQL connection

:param db: correspond sqlalchemy.session
:param db_engine: correspond sqlalchemy.engine
'''

import settings
from utils.db import PostgreSqlConnect

__author__ = 'o.pasichnyk'
__all__ = ['db', 'db_engine', ]

_db_connect = PostgreSqlConnect(settings.DATABASE) #do connect
db = _db_connect.session
db_engine = _db_connect.engine
