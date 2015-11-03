__author__ = 'Bohdan Mushkevych'

import unittest

from odm.errors import ValidationError
from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_nullable_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True)

        model = FieldContainer()
        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

    def test_non_nullable_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False)

        model = FieldContainer()
        try:
            model.validate()
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_non_nullable_default_fields(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False, default=100)

        model = FieldContainer()
        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

    def test_field_choices(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', choices=[1, 2, 3])

        model = FieldContainer()
        try:
            model.field_integer = 1
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

        try:
            model.field_integer = 987
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_field_limits(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', min_value=105.444, max_value=106.987)
            field_integer = fields.IntegerField('i', min_value=100, max_value=250)

        model = FieldContainer()
        try:
            model.field_decimal = 106.1
            model.field_integer = 101
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


if __name__ == '__main__':
    unittest.main()
