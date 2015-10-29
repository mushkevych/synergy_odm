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

    def test_field_choices(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', choices=[1, 2, 3])
            field_string = fields.StringField('s', choices=['111aaa', '222bbb', '333ccc'])

        model = FieldContainer()
        try:
            model.field_integer = 1
            model.field_string = '111aaa'
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

        try:
            model.field_integer = 987
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

        try:
            model.field_string = 'tra'
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_field_limits(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', min_value=105.444, max_value=106.987)
            field_integer = fields.IntegerField('i', min_value=100, max_value=250)
            field_string = fields.StringField('s', min_length=2, max_length=10)

        model = FieldContainer()
        try:
            model.field_decimal = 106.1
            model.field_integer = 101
            model.field_string = 'abc'
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

        try:
            model.field_decimal = 106.99
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

        try:
            model.field_integer = 99
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

        try:
            model.field_string = 'abcdefghijklmnopqrs'
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')


if __name__ == '__main__':
    unittest.main()
