# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['MainHandler', 'RegistrationHandler', 'ErrorHandler', ]

from sqlalchemy.exc import IntegrityError

from db_connect import db
from handlers.base import BaseHandler, form_validator
from forms.users import RegistrationForm
from models.users import User


class MainHandler(BaseHandler):
    def get(self):
        self.render_to_response("index.html")


class RegistrationHandler(BaseHandler):
    def get(self):
        if self.user_id:
            self.redirect("/error")

        self.render_to_response("registration.html", form=RegistrationForm())

    @form_validator(RegistrationForm, raise_http_error=False)
    def post(self, form):
        if self.user_id:
            self.redirect("/error")

        if form.errors:
            self.render_to_response("registration.html", form=form)
            return

        user = User()
        form.populate_obj(user)
        db.add(user)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            self.redirect("/error")
        else:
            self.render_to_response("registration_end.html", name=self.get_argument("name"))


class ErrorHandler(BaseHandler):
    def get(self):
        self.render_to_response("error.html")
