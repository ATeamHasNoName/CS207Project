import os
import json
import unittest
import tempfile
import logging

from app import app
from app.service import APIService

logging.basicConfig(level=logging.DEBUG)

class FlaskServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = APIService('localhost', 5000)
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        # with flaskr.app.app_context():
        #     flaskr.init_db()

    def service_should_retrieve_list_all_tasks(self):
        tasks = self.service.all_tasks()
        logging.debug('Recieved task list %s', tasks)
        assert tasks

    def service_should_add_task_and_return_true(self):
        tasks = self.service.add_task('Do the dishes')
        logging.debug('Recieved task list %s', tasks)
        assert tasks

    # def service_should_remove_task_and_return_true(self):
    #     tasks = self.service.all_tasks()
    #     logging.debug('Recieved task list %s', tasks)
    #     assert tasks

    # def service_should_update_task_and_return_true(self):
    #     tasks = self.service.all_tasks()
    #     logging.debug('Recieved task list %s', tasks)
    #     assert tasks

    def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])
        pass

if __name__ == '__main__':
    unittest.main()
