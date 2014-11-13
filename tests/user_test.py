# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['TestUser', ]

from tests.base import BaseAsyncTestCase
from tests.tests_utils.fixtureman import FixtureManager
from tests.tests_utils.data_provider import data_provider
from models.users import User
from utils.md5_hash import decode_string

user_fixture = FixtureManager()
user_fixture.load(fixture_file='fixtures/user', current_file=__file__)


class TestUser(BaseAsyncTestCase):
    @data_provider(user_fixture['test_registration'])
    def test_registration(self, registration_data, result_has_text):

        request_result = self.request_post('/registration', registration_data)
        self.assertIn(result_has_text, request_result)

    def test_empty_registration(self):
        request_result = self.request_post('/registration', [], body_ckeck=False)
        self.assertEqual(request_result, None)

    @data_provider(user_fixture['test_isset_user'])
    def test_isset_user(self, user_data):
        user = self.add_user(**user_data)

        isset_user = User.isset_user(**user_data)

        self.assertTrue(isset_user)
        self.assertEqual(isset_user['user_name'], user.name)
        self.assertEqual(isset_user['user_id'], user.id)

    @data_provider(user_fixture['test_not_isset_user'])
    def test_not_isset_user(self, user_data):
        isset_user = User.isset_user(**user_data)

        self.assertFalse(isset_user)

    @data_provider(user_fixture['test_is_user_password_hashed'])
    def test_is_user_password_hashed(self, user_data):
        user = self.add_user(**user_data)

        password_hash = decode_string(user_data['password'])

        self.assertTrue(user.password)
        self.assertEqual(user.password, password_hash)
