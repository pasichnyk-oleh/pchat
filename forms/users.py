# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['RegistrationForm', ]

from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired
from wtforms_tornado import Form


class RegistrationForm(Form):
    name = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
