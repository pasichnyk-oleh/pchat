# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['TestingServer', ]

import os

import settings


class TestingServer(object):
    TEST_DB_NAME = 'test2'
    BACKUP_FILE_NAME = 'db_for_test.sql'

    def start(self):
        main_server = os.path.join(settings.PROJECT_DIR, 'index.py')
        python_path = os.path.realpath(os.path.join(settings.PROJECT_DIR, '../python')) # TODO need to be rewriten

        os.system(
            "{python_path} {main_server} --db_name={name} --port={port}".format(
                name=self.TEST_DB_NAME, port=settings.PORT_TEST, main_server=main_server, python_path=python_path)
        )

    def prepare_db(self):
        import settings
        args =  {'backup_file': self.BACKUP_FILE_NAME, 'new_name': self.TEST_DB_NAME}
        args.update(settings.DATABASE)

        export_port = 'export PGPORT=5433'
        pg_dump = 'pg_dump --host={host} --username={user} {name} > {backup_file}'
        psql = 'psql --host={host} --username={user} {new_name} > {backup_file}'
        command = ' %s | %s | %s' % (export_port, pg_dump, psql)

        os.system(command.format(**args))

    def __del__(self):
        os.remove(os.path.join(settings.PROJECT_DIR, self.BACKUP_FILE_NAME))

        # TODO: kill process


if __name__ == "__main__":
    server = TestingServer()

    server.start()
    server.prepare_db()
