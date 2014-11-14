# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['ChatAddForm', 'ChatSearchForm', 'MessageForm', ]

from wtforms.fields import StringField, IntegerField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Length
from wtforms_tornado import Form


class ChatAddForm(Form):
    name = StringField(validators=[DataRequired(Length(1,64))])


class ChatSearchForm(Form):
    name = StringField(validators=[DataRequired(Length(1,64))])


class MessageForm(Form):
    message = StringField(validators=[DataRequired(), Length(1,1024)])
    chat_id = IntegerField(widget=HiddenInput(), validators=[DataRequired(), Length(1,1024)])
