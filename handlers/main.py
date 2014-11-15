# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['MainHandler', 'RegistrationHandler', 'ErrorHandler', ]

from db_connect import db
from handlers.base import BaseHandler, form_validator
from forms.users import RegistrationForm
from models.users import User


class MainHandler(BaseHandler):
    '''Handle main page of app'''
    def get(self):
        self.render_to_response("index.html")


class RegistrationHandler(BaseHandler):
    '''
    Handler to process user registration.
    On GET render registration form and on POST get user registration data and save it
    '''
    def get(self):
        #redirect to main if already logined
        if self.user_id:
            self.redirect("/")

        self.render_to_response("registration.html", form=RegistrationForm())

    @form_validator(RegistrationForm, raise_http_error=False)
    def post(self, form):
        #redirect to main if already logined
        if self.user_id:
            self.redirect("/")

        #if have some errors - again render registration form with errors
        if form.errors:
            self.render_to_response("registration.html", form=form)
            return

        #if all are OK - add user
        user = User()
        form.populate_obj(user)
        db.add(user)
        db.commit()

        self.render_to_response("registration_end.html", name=self.get_argument("name"))


class ErrorHandler(BaseHandler):
    '''Handler for some undefined errors'''
    def get(self):
        self.render_to_response("error.html")
