# coding: utf-8 -*-

import string
import random

__author__ = 'o.pasichnyk'
__all__ = ['random_string', ]


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    '''
    Generate random string

    :param size: int - size of string to generate
    :param chars: list - chars to use in random generating
    :return: str - generated random string
    '''
    return ''.join(random.choice(chars) for _ in range(size))
