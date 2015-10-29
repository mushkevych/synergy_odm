__author__ = 'Bohdan Mushkevych'

import unittest
from odm import document, fields
from odm.errors import ValidationError


class TestDocument(unittest.TestCase):
    def test_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_integer)

    def test_non_nullable_non_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_integer)

    def test_non_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=False, default=123)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertEqual(m2.field_integer, 123)

    def test_nullable_default_jsonification(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True, default=123)

        model = FieldContainer()
        json_data = model.to_json()
        self.assertIsInstance(json_data, dict)
        m2 = FieldContainer.from_json(json_data)

        self.assertIsNone(m2.field_integer)

    def test_nullable_non_default_field(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True)

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
            field_integer = fields.IntegerField('i', null=True, default=999)

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
            field_integer = fields.IntegerField('i', null=False)

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
            field_integer = fields.IntegerField('i', null=False, default=100)

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
            field_integer = fields.IntegerField('i', null=False)

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
            field_integer = fields.IntegerField('i', null=False, default=987654321)

        model = FieldContainer()
        self.assertEqual(model.field_integer, 987654321)

        model.field_integer = 101
        self.assertEqual(model.field_integer, 101)

        model.field_integer = None
        self.assertEqual(model.field_integer, 987654321)

    def test_nullable_non_default_assignment(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        model.field_integer = 101
        self.assertEqual(model.field_integer, 101)

        model.field_integer = None
        self.assertIsNone(model.field_integer)

    def test_nullable_default_assignment(self):
        class FieldContainer(document.BaseDocument):
            field_integer = fields.IntegerField('i', null=True, default=987654321)

        model = FieldContainer()
        self.assertIsNone(model.field_integer)

        model.field_integer = 101
        self.assertEqual(model.field_integer, 101)

        model.field_integer = None
        self.assertIsNone(model.field_integer)


if __name__ == '__main__':
    unittest.main()
