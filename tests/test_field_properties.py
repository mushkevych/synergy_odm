__author__ = 'Bohdan Mushkevych'

import unittest
from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_nullable_non_default_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

    def test_nullable_default_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True, default=999)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

    def test_non_nullable_non_default_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

    def test_non_nullable_default_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False, default=100)

        model = FieldContainer()
        self.assertEqual(model.field_integer, 100)


if __name__ == '__main__':
    unittest.main()
