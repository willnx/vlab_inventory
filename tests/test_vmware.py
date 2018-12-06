# -*- coding: UTF-8 -*-
"""
A set of tests for the vmware.py module
"""
import unittest
from unittest.mock import patch, MagicMock

from vlab_inventory_api.lib.worker import vmware


class TestVMware(unittest.TestCase):
    """A suite of test cases for the vmware.py module"""

    @patch.object(vmware.virtual_machine, 'get_info')
    @patch.object(vmware, 'vCenter')
    def test_show_inventory(self, fake_vCenter, fake_get_info):
        """``show_inventory`` returns a dictionary when the user has VMs"""
        fake_get_info.return_value = {}
        fake_vm = MagicMock()
        fake_vm.name = 'myVM'
        fake_folder = MagicMock()
        fake_folder.childEntity = [fake_vm]
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder

        result = vmware.show_inventory(username='bob')
        expected = {'myVM' : {}}

        self.assertEqual(result, expected)

    @patch.object(vmware, 'vCenter')
    def test_create_inventory(self, fake_vCenter):
        """``create_inventory`` returns None when everything works as expected"""
        result = vmware.create_inventory(username='bob')
        expected = None

        self.assertEqual(result, expected)

    @patch.object(vmware, 'nuke_folder')
    @patch.object(vmware, 'vCenter')
    def test_delete_inventory(self, fake_vCenter, fake_nuke_folder):
        """``delete_inventory`` returns None when everything works as expected"""
        fake_logger = MagicMock()
        fake_folder = MagicMock()
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder

        result = vmware.delete_inventory(username='alice', logger=fake_logger)
        expected = None

        self.assertEqual(result, expected)

    @patch.object(vmware, 'nuke_folder')
    @patch.object(vmware, 'vCenter')
    def test_delete_invalid_power_state(self, fake_vCenter, fake_nuke_folder):
        """``delete_inventory`` returns an error if a VM is not powered off"""
        fake_logger = MagicMock()
        fake_nuke_folder.side_effect = [vmware.vim.fault.InvalidState(msg='testing')]
        fake_folder = MagicMock()
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder

        result = vmware.delete_inventory(username='alice', logger=fake_logger)
        expected = 'testing'

        self.assertEqual(result, expected)

    @patch.object(vmware, 'nuke_folder')
    @patch.object(vmware, 'vCenter')
    def test_delete_already_gone(self, fake_vCenter, fake_nuke_folder):
        """``delete_inventory`` returns an error if the user has no inventory records"""
        fake_logger = MagicMock()
        fake_nuke_folder.side_effect = [FileNotFoundError()]
        fake_folder = MagicMock()
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder

        result = vmware.delete_inventory(username='alice', logger=fake_logger)
        expected = 'User alice has no folder'

        self.assertEqual(result, expected)

    @patch.object(vmware, 'nuke_folder')
    @patch.object(vmware, 'vCenter')
    def test_delete_failure(self, fake_vCenter, fake_nuke_folder):
        """``delete_inventory`` returns an error if there was a system failure"""
        fake_logger = MagicMock()
        fake_nuke_folder.side_effect = [RuntimeError('testing')]
        fake_folder = MagicMock()
        fake_vCenter.return_value.__enter__.return_value.get_by_name.return_value = fake_folder

        result = vmware.delete_inventory(username='alice', logger=fake_logger)
        expected = 'testing'

        self.assertEqual(result, expected)

    @patch.object(vmware, 'consume_task')
    def test_nuke_folder(self, fake_consume_task):
        """``nuke_folder`` calls Destory on the folder object"""
        fake_folder = MagicMock()

        vmware.nuke_folder(fake_folder)

        self.assertTrue(fake_folder.Destroy.called)


if __name__ == '__main__':
    unittest.main()
