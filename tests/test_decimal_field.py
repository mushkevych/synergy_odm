# -*- coding: utf-8 -*-
__author__ = 'Bohdan Mushkevych'

import unittest

from odm import document, fields
from odm.errors import ValidationError

DEFAULT_VALUE = 987.65


class TestDocument(unittest.TestCase):
    def test_valid_inputs(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=False, precision=7)

        fixtures = {
            '1': 1,
            1: 1,
            150.001: 150.001,
            '7654321.1234567': 7654321.1234567,
        }

        model = FieldContainer()
        for key, value in fixtures.items():
            model.field_decimal = key
            self.assertEqual(model.field_decimal, value)

    def test_constraints(self):
        min_value = 5.01
        max_value = 9876543210.97

        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', min_value=min_value, max_value=max_value)

        valid_middle = (min_value + max_value) / 2.0
        invalid_min = min_value - 0.01
        invalid_max = max_value + 0.01

        model = FieldContainer()
        for value in [min_value, valid_middle, max_value]:
            model.field_decimal = value
            self.assertEqual(model.field_decimal, value)

        for value in [invalid_min, invalid_max]:
            try:
                model.field_decimal = value
                self.assertTrue(False, 'ValidationError should have been thrown')
            except ValidationError:
                self.assertTrue(True, 'ValidationError was expected and caught')

    def test_choices(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('s', choices=[123.45, 456.78, 987])

        model = FieldContainer()
        model.field_decimal = '123.45'
        self.assertEqual(model.field_decimal, 123.45)

        model.field_decimal = 987
        self.assertEqual(model.field_decimal, 987)

        try:
            model.field_decimal = '1122'
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_precision(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=False, precision=1)

        fixtures = {
            '1': 1,
            1: 1,
            150.001: 150,
            '7654321.1234567': 7654321.1,
        }

        model = FieldContainer()
        for key, value in fixtures.items():
            model.field_decimal = key
            self.assertEqual(model.field_decimal, value)

    def test_force_string(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=False, precision=5, force_string=True)

        fixtures = {
            '1': '1.00000',
            1: '1.00000',
            150.001: '150.00100',
            '7654321.1234567': '7654321.12346',
        }

        model = FieldContainer()
        for key, value in fixtures.items():
            model.field_decimal = key
            self.assertEqual(model.field_decimal, value)

    def test_force_string_choices(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('s', choices=[123.45, 456.78, 987], force_string=True)

        model = FieldContainer()
        model.field_decimal = '123.45'
        self.assertEqual(model.field_decimal, '123.45')

        model.field_decimal = 987
        self.assertEqual(model.field_decimal, '987.00')

        try:
            model.field_decimal = '1122'
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_nullable_non_default(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=True)

        model = FieldContainer()

        try:
            model.validate()
            self.assertTrue(True, 'Validation should succeed')
        except ValidationError:
            self.assertTrue(False, 'ValidationError should not have been thrown')

        model.field_decimal = None
        self.assertTrue(True, 'Validation should succeed')

    def test_non_nullable_non_default(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=False)

        model = FieldContainer()
        try:
            model.validate()
            self.assertTrue(False, 'Validation should have failed')
        except ValidationError:
            self.assertTrue(True, 'ValidationError should not have been thrown')

        model.field_decimal = 123.654
        self.assertEqual(model.field_decimal, 123.65)

        try:
            model.field_decimal = None
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_non_nullable_default(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=False, default=DEFAULT_VALUE)

        model = FieldContainer()
        self.assertEqual(model.field_decimal, DEFAULT_VALUE)

    def test_nullable_default(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=True, default=DEFAULT_VALUE)

        model = FieldContainer()
        self.assertIsNone(model.field_decimal)

        model.field_decimal = None
        self.assertIsNone(model.field_decimal)

    def test_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=True)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_decimal)

    def test_non_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=False)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_decimal)

    def test_non_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=False, default=DEFAULT_VALUE)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertEqual(m2.field_decimal, DEFAULT_VALUE)

    def test_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_decimal = fields.DecimalField('d', null=True, default=DEFAULT_VALUE)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_decimal)


if __name__ == '__main__':
    unittest.main()
