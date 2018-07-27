# -*- coding: UTF-8 -*-
"""
A suite of tests for the functions in tasks.py
"""
import unittest
from unittest.mock import patch, MagicMock

from vlab_inventory_api.lib.worker import tasks


class TestTasks(unittest.TestCase):
    """A set of test cases for tasks.py"""
    @patch.object(tasks, 'vmware')
    def test_show_ok(self, fake_vmware):
        """``show`` returns a dictionary when everything works as expected"""
        fake_vmware.show_inventory.return_value = {'worked': True}

        output = tasks.show(username='bob')
        expected = {'content' : {'worked': True}, 'error': None, 'params': {}}

        self.assertEqual(output, expected)

    @patch.object(tasks, 'vmware')
    def test_show_value_error(self, fake_vmware):
        """``show`` sets the error in the dictionary when catching FileNotFoundError exception"""
        fake_vmware.show_inventory.side_effect = [FileNotFoundError("testing")]

        output = tasks.show(username='bob')
        expected = {'content' : {}, 'error': 'User bob has no folder; try POSTing to create one.', 'params': {}}

        self.assertEqual(output, expected)

    @patch.object(tasks, 'vmware')
    def test_create_ok(self, fake_vmware):
        """``create`` returns a dictionary when everything works as expected"""
        output = tasks.create(username='bob')
        expected = {'content' : {}, 'error': None, 'params': {}}

        self.assertEqual(output, expected)

    @patch.object(tasks, 'vmware')
    def test_delete_ok(self, fake_vmware):
        """``delete`` returns a dictionary when everything works as expected"""
        fake_vmware.delete_inventory.return_value = None

        output = tasks.delete(username='bob')
        expected = {'content' : {}, 'error': None, 'params': {}}

        self.assertEqual(output, expected)

    @patch.object(tasks, 'vmware')
    def test_delete_value_error(self, fake_vmware):
        """``delete`` sets the error in the dictionary when there's an error"""
        fake_vmware.delete_inventory.return_value = "someError"

        output = tasks.delete(username='bob')
        expected = {'content' : {}, 'error': 'someError', 'params': {}}

        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
