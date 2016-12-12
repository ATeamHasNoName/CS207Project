import os
import json
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        # with flaskr.app.app_context():
        #     flaskr.init_db()

    def test_delete(self):
        rv = self.app.delete('/tasks')
        json_response = json.loads(rv.data)
        assert json_response["op"]

    def test_empty_db(self):
        rv = self.app.get('/tasks')
        json_response = json.loads(rv.data)
        assert not json_response["tasks"]

    def test_insert_and_get(self):
        rv = self.app.post(
            '/tasks',
            data=json.dumps({"action": "Go to Grocery Store"}),
            headers={'content-type':'application/json'}
        )
        json_response = json.loads(rv.data)
        assert json_response["task"]
        assert json_response["op"]

        rv = self.app.get('/tasks/1')
        json_response = json.loads(rv.data)
        assert json_response["task"]
        # assert json_response["op"]

    def test_insert_and_update(self):
        rv = self.app.post(
            '/tasks',
            data=json.dumps({"action": "Go to Grocery Store"}),
            headers={'content-type':'application/json'}
        )
        json_response = json.loads(rv.data)
        assert json_response["task"]
        assert json_response["op"]

        task_id = json_response["task"]["task_id"]
        rv = self.app.put(
            '/tasks/1',
            data=json.dumps({"action": "Go to Grocery Store and get cheese"}),
            headers={'content-type':'application/json'}
        )
        json_response = json.loads(rv.data)
        assert json_response["task"]
        # assert json_response["op"]

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
