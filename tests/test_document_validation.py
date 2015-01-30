__author__ = 'Bohdan Mushkevych'

import unittest

from odm.errors import ValidationError
from odm import document, fields
from tests.test_simple_document import SimpleContainer


class FieldContainer(document.BaseDocument):
    field_nested_nullable = fields.NestedDocumentField('nested', SimpleContainer, null=True)
    field_nested_non_null = fields.NestedDocumentField('nested', SimpleContainer, null=False)
    field_int_1 = fields.IntegerField('i1', null=False)
    field_int_2 = fields.IntegerField('i2', null=True)
    field_int_3 = fields.IntegerField('i3', null=False)
    field_string_null = fields.StringField('s')
    field_string = fields.StringField('s')


class TestDocument(unittest.TestCase):
    def test_nullable(self):
        class FieldContainer(document.BaseDocument):
            field_nested_nullable = fields.NestedDocumentField('nested', SimpleContainer, null=True)
            field_string = fields.StringField('s', null=False)

        model = FieldContainer()
        model.field_string = 'first-level string field'

        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

    def test_non_nullable(self):
        class FieldContainer(document.BaseDocument):
            field_nested_non_null = fields.NestedDocumentField('nested', SimpleContainer, null=False)
            field_string = fields.StringField('s', null=False)

        model = FieldContainer()
        model.field_string = 'first-level string field'

        try:
            model.validate()
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_nullable_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True)
            field_string = fields.StringField('s', null=True)

        model = FieldContainer()

        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

    def test_non_nullable_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False)
            field_string = fields.StringField('s', null=False)

        model = FieldContainer()
        model.field_string = 'first-level string field'

        try:
            model.validate()
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')


if __name__ == '__main__':
    unittest.main()
