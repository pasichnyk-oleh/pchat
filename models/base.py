# coding: utf-8 -*-

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'o.pasichnyk'
__all__ = ['Base', ]


class _BaseModel(object):
    '''Base abstrat model, that add default primary key id field'''
    __abstract__ = True

    id = Column(Integer, primary_key = True)

Base = declarative_base(cls=_BaseModel)
