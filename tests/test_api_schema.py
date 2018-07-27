# -*- coding: UTF-8 -*-
"""
A suite of tests for the HTTP API schemas
"""
import unittest

from jsonschema import Draft4Validator, validate, ValidationError
from vlab_inventory_api.lib.views import inventory


class TestInventoryViewSchema(unittest.TestCase):
    """A set of tes cases for the schemas in /api/1/inf/inventory end points"""

    def test_post_schema(self):
        """The schema defined for POST on /api/1/inf/inventory is a valid schema"""
        try:
            Draft4Validator.check_schema(inventory.InventoryView.POST_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)

    def test_get_schema(self):
        """The schema defined for GET on /api/1/inf/inventory is a valid schema"""
        try:
            Draft4Validator.check_schema(inventory.InventoryView.GET_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)

    def test_delete_schema(self):
        """The schema defined for DELETE on /api/1/inf/inventory is a valid schema"""
        try:
            Draft4Validator.check_schema(inventory.InventoryView.DELETE_SCHEMA)
            schema_valid = True
        except RuntimeError:
            schema_valid = False

        self.assertTrue(schema_valid)


if __name__ == '__main__':
    unittest.main()
