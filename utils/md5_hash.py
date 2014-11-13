# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['decode_string']

import hashlib


def decode_string(string, salt='abc'):
    '''
    Decode string to md5 hash + some salt

    :param string: string to decode
    :param salt:  salt to add at begin and end of string
    :return: hashed string
    '''
    new_string = '{salt}{string}{salt}'.format(salt=salt, string=string)

    return hashlib.md5(new_string).hexdigest()
