# coding: utf-8 -*-

import string
import random

__author__ = 'o.pasichnyk'
__all__ = ['random_string', ]


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
