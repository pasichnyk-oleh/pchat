# coding: utf-8 -*-

from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp
from wtforms_tornado import Form

from models.users import User
from db_connect import db

__author__ = 'o.pasichnyk'
__all__ = ['RegistrationForm', ]


class RegistrationForm(Form):
    name = StringField(validators=[DataRequired(), Regexp("([A-z0-9]){2,20}",
                                                          message="Must contain only A-Z, a-z, 0-9, length 2-20")])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('confirm_password', message='Your passwords did not match'),
                                         Length(min=6, max=20, message='Passwords must be longer than 6 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

    def validate_name(self, field):
        if db.query(User).filter(User.name==field.data).first():
            raise ValidationError('Username already exists')
