# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['db', 'db_engine', ]

import settings
from utils.db import PostgreSqlConnect


_db_connect = PostgreSqlConnect(settings.DATABASE)
db = _db_connect.session
db_engine = _db_connect.engine
