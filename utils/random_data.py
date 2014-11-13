# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['random_string', ]

import string
import random

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
