# -*- coding: utf-8 -*-

import json
import os

__author__ = 'o.pasichnyk'
__all__ = ['FixtureManager', ]


class FixtureManager(object):
    def __init__(self):
        self.fixture_data = {}

    def load(self, fixture_data=None, fixture_file=None, file_ext='json', current_file=__file__):
        """
        Load fixtures from iterable (list, dict, tuple, ...) instance (fixture_data) or file

        :param fixture_data: iterable - iterable data container
        :param fixture_file: string - name of file, from where will be loaded data.
        :param file_ext: string - extension of file without(!) leading dot. If empty string or None - no
                        additional extensions used
        :param current_file: string - file, indicates from where need to search relative path of fixture_file

        :raise ImportError: - if fixture data source is undefined
        """
        if fixture_data is not None:
            self.fixture_data = fixture_data
        elif fixture_file is not None:
            if file_ext:
                fixture_file += '.' + file_ext
            with open(self.get_fixture_path(fixture_file, current_file), 'r') as fp:
                self.fixture_data = json.load(fp)
        else:
            raise ImportError('Undefined fixture data source')

    def get(self, fixture_name):
        """
        Get fixture data by it's name.

        :param fixture_name: string - name of fixture, which data need to return
        :return: dict - if fixture_name doesn't exists - will be returned an empty dict
        """
        return self.fixture_data[fixture_name] if fixture_name in self.fixture_data else dict

    def __getitem__(self, item):
        return self.get(item)

    @classmethod
    def get_fixture_path(cls, fixture_file, current_file=__file__):
        """
        Build and return absolute path to the fixture's file.

        :note: method doesn't check existence of file

        :param fixture_file: string - name of file, from where will be loaded data.
        :param current_file: string - file, indicates from where need to search relative path of fixture_file

        :return: string
        """
        return os.path.join(os.path.abspath(os.path.dirname(current_file)), *('', fixture_file,))