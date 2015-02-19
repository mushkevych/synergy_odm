__author__ = 'Bohdan Mushkevych'

import unittest

from odm.errors import ValidationError
from odm import document, fields
from tests.test_simple_fields import SimpleContainer


class TestDocument(unittest.TestCase):
    def test_nullable_nested_docs(self):
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

    def test_non_nullable_nested_docs(self):
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

    def test_non_nullable_default_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False, default=100)
            field_string = fields.StringField('s', null=False, default='default string')
            field_string_empty = fields.StringField('empty', null=False, default='')

        model = FieldContainer()
        model.field_string = 'first-level string field'

        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')


if __name__ == '__main__':
    unittest.main()
