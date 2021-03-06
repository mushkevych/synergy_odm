__author__ = 'Bohdan Mushkevych'

import unittest
from datetime import datetime, timedelta

from odm import document, fields
from tests.test_document_operations import SimpleContainer


class NestedNullableDocuments(document.BaseDocument):
    field_nested = fields.NestedDocumentField(SimpleContainer, null=True)
    field_integer = fields.IntegerField(name='i')


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.model = NestedNullableDocuments()

    def tearDown(self):
        del self.model

    def test_getter_setter(self):
        self.model.field_integer = 123456789
        try:
            self.model.field_nested.field_boolean = True
            self.assertTrue(False, 'AttributeError should have been thrown')
        except AttributeError:
            self.assertTrue(True, 'AttributeError was expected and caught')

    def test_init_jsonification(self):
        now = datetime.now()

        self.model.field_integer = 123456789
        self.model.field_nested = SimpleContainer()
        self.model.field_nested.field_boolean = True
        self.model.field_nested.field_string = 'a short string description'
        self.model.field_nested.field_datetime = now
        self.model.field_nested.field_decimal = 123.123
        self.model.field_nested.field_integer = 123

        json_data = self.model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = NestedNullableDocuments.from_json(json_data)

        self.assertEqual(self.model.field_integer, m2.field_integer)
        self.assertEqual(self.model.field_nested.field_boolean, m2.field_nested.field_boolean)
        self.assertTrue(self.model.field_nested.field_datetime - m2.field_nested.field_datetime < timedelta(seconds=1))
        self.assertAlmostEqual(self.model.field_nested.field_decimal, float(m2.field_nested.field_decimal), delta=0.01)
        self.assertEqual(self.model.field_nested.field_integer, m2.field_nested.field_integer)
        self.assertEqual(self.model.field_nested.field_string, m2.field_nested.field_string)

        self.model.field_nested.field_integer = 999
        self.assertNotEqual(self.model.field_nested.field_integer, m2.field_nested.field_integer)

    def test_null_jsonification(self):
        self.model.field_integer = 123456789

        json_data = self.model.to_json()
        self.assertIsNone(self.model.field_nested)
        self.assertIsInstance(json_data, dict)
        m2 = NestedNullableDocuments.from_json(json_data)

        self.assertEqual(self.model.field_integer, m2.field_integer)
        self.assertIsNone(m2.field_nested)


if __name__ == '__main__':
    unittest.main()
