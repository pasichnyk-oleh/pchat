# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['TestImageFindHandler', ]

from mock import MagicMock

from tests.base import BaseAsyncTestCase
from tests.tests_utils.fixtureman import FixtureManager
from tests.tests_utils.data_provider import data_provider
from models.field_handlers import ImageFindHandler, Md5Handler

field_handlers_fixture = FixtureManager()
field_handlers_fixture.load(fixture_file='fixtures/field_handlers', current_file=__file__)


class TestImageFindHandler(BaseAsyncTestCase):
    @data_provider(field_handlers_fixture['test_image_hander'])
    def test_image_hander(self, text_to_process, img_path, mime_type, text_to_assert_in):
        if img_path:
            img_path = "%s/%s" % (self.server_url, img_path)
            text_to_process = text_to_process.format(img_path)
            text_to_assert_in = text_to_assert_in.format(img_path)

        handler = ImageFindHandler()
        handler._get_url_mime = MagicMock(return_value=mime_type)
        handler._get_and_save_content = MagicMock(return_value=img_path)

        handler_result = handler.process(text_to_process)

        self.assertIn(text_to_assert_in, handler_result)


class TestMd5Handler(BaseAsyncTestCase):
    @data_provider(field_handlers_fixture['test_md5_handler'])
    def test_md5_handler(self, text_to_process, salt, text_to_compare):
        handler = Md5Handler(salt)

        result = handler.process(text_to_process)

        self.assertEqual(result, text_to_compare)
