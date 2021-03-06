__author__ = 'Bohdan Mushkevych'

import unittest
from datetime import datetime, timedelta

from odm import document, fields
from odm.errors import ValidationError
from tests.test_document_operations import SimpleContainer


class NestedDocuments(document.BaseDocument):
    field_nested = fields.NestedDocumentField(SimpleContainer)
    field_integer = fields.IntegerField()


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.model = NestedDocuments()

    def tearDown(self):
        del self.model

    def test_nullable_nested_docs(self):
        class FieldContainer(document.BaseDocument):
            field_nested_nullable = fields.NestedDocumentField(SimpleContainer, name='nested', null=True)
            field_string = fields.StringField(null=False)

        model = FieldContainer()
        model.field_string = 'first-level string field'

        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

    def test_non_nullable_nested_docs(self):
        class FieldContainer(document.BaseDocument):
            field_nested_non_null = fields.NestedDocumentField(SimpleContainer, name='nested', null=False)
            field_string = fields.StringField(name='s', null=False)

        model = FieldContainer()
        model.field_string = 'first-level string field'

        try:
            model.validate()
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_getter_setter(self):
        now = datetime.now()

        self.model.field_integer = 123456789
        self.model.field_nested.field_boolean = True
        self.model.field_nested.field_string = 'a short string description'
        self.model.field_nested.field_datetime = now
        self.model.field_nested.field_decimal = 123.123
        self.model.field_nested.field_integer = 123

        self.assertEqual(self.model.field_integer, 123456789)
        self.assertTrue(self.model.field_nested.field_boolean)
        self.assertEqual(self.model.field_nested.field_datetime, now)
        self.assertEqual(self.model.field_nested.field_decimal, 123.123)
        self.assertEqual(self.model.field_nested.field_integer, 123)
        self.assertEqual(self.model.field_nested.field_string, 'a short string description')

    def test_jsonification(self):
        now = datetime.now()

        self.model.field_integer = 123456789
        self.model.field_nested.field_boolean = True
        self.model.field_nested.field_string = 'a short string description'
        self.model.field_nested.field_datetime = now
        self.model.field_nested.field_decimal = 123.123
        self.model.field_nested.field_integer = 123

        json_data = self.model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = NestedDocuments.from_json(json_data)

        self.assertEqual(self.model.field_integer, m2.field_integer)
        self.assertEqual(self.model.field_nested.field_boolean, m2.field_nested.field_boolean)
        self.assertTrue(self.model.field_nested.field_datetime - m2.field_nested.field_datetime < timedelta(seconds=1))
        self.assertAlmostEqual(self.model.field_nested.field_decimal, float(m2.field_nested.field_decimal), delta=0.01)
        self.assertEqual(self.model.field_nested.field_integer, m2.field_nested.field_integer)
        self.assertEqual(self.model.field_nested.field_string, m2.field_nested.field_string)

        self.model.field_nested.field_integer = 999
        self.assertNotEqual(self.model.field_nested.field_integer, m2.field_nested.field_integer)


if __name__ == '__main__':
    unittest.main()
