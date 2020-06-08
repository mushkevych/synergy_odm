__author__ = 'Bohdan Mushkevych'

import unittest

from odm.errors import ValidationError
from odm import document, fields


class TestDocument(unittest.TestCase):
    def test_choices(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(choices=[1, 2, 3])

        model = FieldContainer()
        model.field_integer = 1
        self.assertEqual(model.field_integer, 1)

        try:
            model.field_integer = 987
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_constraints(self):
        min_value = 5
        max_value = 9876543210

        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(min_value=min_value, max_value=max_value)

        valid_middle = int((min_value + max_value) / 2)
        invalid_min = min_value - 1
        invalid_max = max_value + 1

        model = FieldContainer()
        for value in [min_value, valid_middle, max_value]:
            model.field_integer = value
            self.assertEqual(model.field_integer, value)

        for value in [invalid_min, invalid_max]:
            try:
                model.field_integer = value
                self.assertTrue(False, 'ValidationError should have been thrown')
            except ValidationError:
                self.assertTrue(True, 'ValidationError was expected and caught')

    def test_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=True)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_integer)

    def test_non_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=False)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_integer)

    def test_non_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=False, default=123)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertEqual(m2.field_integer, 123)

    def test_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=True, default=123)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_integer)

    def test_nullable_non_default_field(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=True)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        del model.field_integer
        self.assertIsNone(model.field_integer)

        model.field_integer = 789
        self.assertEqual(model.field_integer, 789)

        del model.field_integer
        self.assertIsNone(model.field_integer)

    def test_nullable_default_field(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=True, default=999)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        del model.field_integer
        self.assertIsNone(model.field_integer)

        model.field_integer = 789
        self.assertEqual(model.field_integer, 789)

        del model.field_integer
        self.assertEqual(model.field_integer, 999)

    def test_non_nullable_non_default_field(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=False)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        del model.field_integer
        self.assertIsNone(model.field_integer)

        model.field_integer = 789
        self.assertEqual(model.field_integer, 789)

        del model.field_integer
        self.assertIsNone(model.field_integer)

    def test_non_nullable_default_field(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=False, default=100)

        model = FieldContainer()
        self.assertEqual(model.field_integer, 100)

        del model.field_integer
        self.assertEqual(model.field_integer, 100)

        model.field_integer = 789
        self.assertEqual(model.field_integer, 789)

        del model.field_integer
        self.assertEqual(model.field_integer, 100)

    def test_non_nullable_non_default_assignment(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=False)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        model.field_integer = 101
        self.assertEqual(model.field_integer, 101)

        try:
            model.field_integer = None
            self.assertTrue(False, 'ValidationError should have been thrown')
        except ValidationError:
            self.assertTrue(True, 'ValidationError was expected and caught')

    def test_non_nullable_default_assignment(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=False, default=987654321)

        model = FieldContainer()
        self.assertEqual(model.field_integer, 987654321)

        model.field_integer = 101
        self.assertEqual(model.field_integer, 101)

        model.field_integer = None
        self.assertEqual(model.field_integer, 987654321)

    def test_nullable_non_default_assignment(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=True)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        model.field_integer = 101
        self.assertEqual(model.field_integer, 101)

        model.field_integer = None
        self.assertIsNone(model.field_integer)

    def test_nullable_default_assignment(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField(null=True, default=987654321)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        model.field_integer = 101
        self.assertEqual(model.field_integer, 101)

        model.field_integer = None
        self.assertIsNone(model.field_integer)


if __name__ == '__main__':
    unittest.main()
