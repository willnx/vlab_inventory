# -*- coding: UTF-8 -*-
"""
Unittest for the RESTful API of /api/1/inf/inventory end point
"""
import unittest
from unittest.mock import patch, MagicMock

from flask import Flask
from vlab_api_common.http_auth import generate_v2_test_token

import vlab_inventory_api.app as inventory_app
from vlab_inventory_api.lib.views import inventory


class TestInventoryView(unittest.TestCase):
    """Test suite for InventoryView"""

    @classmethod
    def setUpClass(cls):
        """Runs once, before any test case"""
        cls.token = generate_v2_test_token(username='bob')

    @classmethod
    def setUp(cls):
        app = Flask(__name__)
        inventory.InventoryView.register(app)
        inventory_app.app.config['TESTING'] = True
        cls.app = app.test_client()
        # Mock Celery
        app.celery_app = MagicMock()
        cls.fake_task = MagicMock()
        cls.fake_task.id = 'asdf-asdf-asdf'
        app.celery_app.send_task.return_value = cls.fake_task

    def test_get_task_id(self):
        """GET on /api/1/inf/inventory returns a task-id when given valid input"""
        resp = self.app.get('/api/1/inf/inventory', headers={'X-Auth': self.token})

        result = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(result, expected)

    def test_get_task_link(self):
        """GET on /api/1/inf/inventory sets the Link header"""
        resp = self.app.get('/api/1/inf/inventory', headers={'X-Auth': self.token})

        task_id = resp.headers['Link']
        expected = '<https://localhost/api/1/inf/inventory/task/asdf-asdf-asdf>; rel=status'

        self.assertEqual(task_id, expected)

    def test_post_task_id(self):
        """POST on /api/1/inf/inventory turns a task-id when given valid input"""
        resp = self.app.post('/api/1/inf/inventory', headers={'X-Auth': self.token})

        result = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(result, expected)

    def test_post_task_link(self):
        """POST on /api/1/inf/inventory sets the Link header"""
        resp = self.app.post('/api/1/inf/inventory', headers={'X-Auth': self.token})

        task_id = resp.headers['Link']
        expected = '<https://localhost/api/1/inf/inventory/task/asdf-asdf-asdf>; rel=status'

        self.assertEqual(task_id, expected)

    def test_delete_task_id(self):
        """DELETE on /api/1/inf/inventory turns a task-id when given valid input"""
        resp = self.app.delete('/api/1/inf/inventory', headers={'X-Auth': self.token})

        result = resp.json['content']['task-id']
        expected = 'asdf-asdf-asdf'

        self.assertEqual(result, expected)

    def test_delete_task_link(self):
        """DELETE on /api/1/inf/inventory sets the Link header"""
        resp = self.app.delete('/api/1/inf/inventory', headers={'X-Auth': self.token})

        task_id = resp.headers['Link']
        expected = '<https://localhost/api/1/inf/inventory/task/asdf-asdf-asdf>; rel=status'

        self.assertEqual(task_id, expected)

    def test_network(self):
        """GatewayView - PUT on /api/1/inf/inventory returns a 404"""
        resp = self.app.put('/api/1/inf/inventory/network',
                            headers={'X-Auth': self.token})

        status = resp.status_code
        expected = 404

        self.assertEqual(status, expected)


if __name__ == '__main__':
    unittest.main()
